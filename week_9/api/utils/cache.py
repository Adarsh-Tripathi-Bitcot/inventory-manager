from datetime import datetime, timezone, timedelta
from ..models import LLMCache
from ..db import db
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

CACHE_EXPIRATION_MINUTES = 60


def get_cached_response(model_name: str, prompt: str, user_id: int | None) -> str | None:
    """Return cached response for a specific user (or global if user_id is None) if not expired."""
    try:
        cache_entry = LLMCache.query.filter_by(model_name=model_name, prompt=prompt, user_id=user_id).first()
        if cache_entry:
            if not cache_entry.is_expired():
                logger.info("Cache HIT for model=%s prompt='%s' user_id=%s", model_name, prompt, user_id)
                return cache_entry.response
            else:
                logger.info("Cache EXPIRED for model=%s prompt='%s' user_id=%s", model_name, prompt, user_id)
        else:
            logger.info("Cache MISS for model=%s prompt='%s' user_id=%s", model_name, prompt, user_id)
        return None
    except Exception as e:
        logger.error("Cache lookup error: %s", e)
        return None


def set_cached_response(model_name: str, prompt: str, response: str, user_id: int | None, expiration_minutes: int = CACHE_EXPIRATION_MINUTES):
    """Upsert a cache entry for the given user/model/prompt tuple."""
    try:
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
        # Use SQL upsert for safety/performance
        stmt = text(
            """
            INSERT INTO llm_cache (model_name, prompt, response, user_id, created_at, expiration_time)
            VALUES (:model_name, :prompt, :response, :user_id, :created_at, :expiration_time)
            ON CONFLICT (model_name, prompt, user_id)
            DO UPDATE SET response = EXCLUDED.response, created_at = EXCLUDED.created_at, expiration_time = EXCLUDED.expiration_time
            RETURNING id;
            """
        )
        params = {
            "model_name": model_name,
            "prompt": prompt,
            "response": response,
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc),
            "expiration_time": expiration_time,
        }
        db.session.execute(stmt, params)
        db.session.commit()
        logger.info("Cache upserted for user_id=%s model=%s", user_id, model_name)
    except Exception as e:
        db.session.rollback()
        logger.error("Error upserting cache: %s", e)


def invalidate_user_cache(user_id: int):
    """Invalidate (delete) all cache rows for a user. Called when user uploads/updates docs."""
    try:
        db.session.query(LLMCache).filter(LLMCache.user_id == user_id).delete()
        db.session.commit()
        logger.info("Invalidated cache for user_id=%s", user_id)
    except Exception as e:
        db.session.rollback()
        logger.error("Failed to invalidate cache for user_id=%s: %s", user_id, e)