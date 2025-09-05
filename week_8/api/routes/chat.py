"""Chat-related API routes for RAG-based Q&A."""

from flask import Blueprint, request, jsonify
from ..utils.security import jwt_required
from week_8.scripts.rag_bot import load_vector_store, build_rag_chain

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# Load RAG chain once at startup (avoid rebuilding on every request)
_vector_store = load_vector_store()
_rag_chain = build_rag_chain(_vector_store)


@chat_bp.route("/inventory", methods=["POST"])
@jwt_required
def chat_inventory():
    """Answer inventory-related questions using RAG.

    Expected JSON body:
        {
            "question": "<str>"
        }

    Returns:
        {
            "answer": "<str>"
        }
    """
    data = request.get_json(force=True, silent=True)
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question: str = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    try:
        answer: str = _rag_chain.invoke(question)
        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
