from __future__ import annotations

from flask import Blueprint, request, jsonify
from ..utils.security import jwt_required, get_current_user
from ..utils.cache import invalidate_user_cache
from ..models import Document as DocumentModel
from ..db import db
from langchain.text_splitter import RecursiveCharacterTextSplitter
from week_9.scripts.rag_bot import load_vector_store
from week_9.api.constants import CHUNK_SIZE, CHUNK_OVERLAP
import logging

bp = Blueprint("documents", __name__, url_prefix="/documents")
logger = logging.getLogger(__name__)


def _get_user_vs():
    # Lazy load to avoid DATABASE_URL lookup at import time
    return load_vector_store(collection_name="user_embeddings_hf")


@bp.route("/upload", methods=["POST"])
@jwt_required
def upload_document():
    """Upload a text file, store raw in DB, chunk+embed to PGVector with user_id metadata, and invalidate user cache."""
    user = get_current_user()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        content_type = file.mimetype or "text/plain"
        raw_bytes = file.read()
        try:
            text = raw_bytes.decode("utf-8")
        except Exception:
            # fallback
            text = raw_bytes.decode("latin-1", errors="ignore")

        # 1) Persist original document
        doc_row = DocumentModel(
            user_id=int(user.id),
            filename=file.filename,
            content_type=content_type,
            text=text,
        )
        db.session.add(doc_row)
        db.session.commit()

        # 2) Chunk and embed to PGVector with metadata
        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = [c for c in splitter.split_text(text) if c.strip()]

        if chunks:
            metadatas = [
                {"user_id": int(user.id), "filename": file.filename, "doc_id": int(doc_row.id)}
                for _ in chunks
            ]
            _get_user_vs().add_texts(texts=chunks, metadatas=metadatas)

        # 3) Invalidate cache for this user
        invalidate_user_cache(int(user.id))

        return jsonify({
            "message": "File uploaded and embedded",
            "doc_id": int(doc_row.id),
            "chunks": len(chunks),
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error("Upload failed: %s", e)
        return jsonify({"error": str(e)}), 500


