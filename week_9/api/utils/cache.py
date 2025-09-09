from datetime import datetime, timezone, timedelta
from ..models import LLMCache
from ..db import db
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

CACHE_EXPIRATION_MINUTES = 60

def get_cached_response(model_name: str, prompt: str) -> str | None:
    """Return cached response if available and not expired."""
    cache_entry = LLMCache.query.filter_by(model_name=model_name, prompt=prompt).first()
    if cache_entry:
        if not cache_entry.is_expired():
            logger.info(f"Cache HIT for prompt: '{prompt}'")
            return cache_entry.response
        else:
            logger.info(f"Cache EXPIRED for prompt: '{prompt}'")
    else:
        logger.info(f"Cache MISS for prompt: '{prompt}'")
    return None


def set_cached_response(model_name: str, prompt: str, response: str, expiration_minutes: int = CACHE_EXPIRATION_MINUTES):
    """Insert or update cache using PostgreSQL ON CONFLICT (UPSERT)."""
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)

    sql = text("""
    INSERT INTO llm_cache (model_name, prompt, response, created_at, expiration_time)
    VALUES (:model_name, :prompt, :response, :created_at, :expiration_time)
    ON CONFLICT (prompt)
    DO UPDATE SET
        response = EXCLUDED.response,
        created_at = EXCLUDED.created_at,
        expiration_time = EXCLUDED.expiration_time
    RETURNING id;
    """)

    params = {
        "model_name": model_name,
        "prompt": prompt,
        "response": response,
        "created_at": datetime.now(timezone.utc),
        "expiration_time": expiration_time,
    }

    try:
        db.session.execute(sql, params)
        db.session.commit()
        logger.info(f"Cache UPSERTED for prompt: '{prompt}'")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error upserting cache for prompt '{prompt}': {str(e)}")