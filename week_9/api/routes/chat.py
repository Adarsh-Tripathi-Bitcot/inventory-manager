from flask import Blueprint, request, jsonify
from ..utils.security import jwt_required, get_current_user
from week_9.scripts.rag_bot import load_vector_store, build_rag_chain
from ..utils.cache import get_cached_response, set_cached_response
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


class CombinedRetriever:
    """Simple retriever that merges user-specific docs and global product docs."""

    def __init__(
        self,
        user_vs,
        product_vs,
        user_id: int,
        k_user: int = 5,
        k_product: int = 3,
        min_relevance: float = 0.5,
    ):
        self.user_vs = user_vs
        self.product_vs = product_vs
        self.user_id = user_id
        self.k_user = k_user
        self.k_product = k_product
        self.min_relevance = min_relevance

    def get_relevant_documents(self, query: str) -> List[Document]:
        # Retrieve user docs filtered by user_id metadata with relevance scores
        user_docs: List[Document] = []
        try:
            if hasattr(self.user_vs, "similarity_search_with_relevance_scores"):
                pairs = self.user_vs.similarity_search_with_relevance_scores(
                    query, k=self.k_user, filter={"user_id": self.user_id}
                )
                user_docs = [
                    doc for doc, score in pairs if (score or 0) >= self.min_relevance
                ]
            else:
                user_docs = self.user_vs.similarity_search(
                    query, k=self.k_user, filter={"user_id": self.user_id}
                )
        except Exception:
            user_docs = []

        # Retrieve global product docs (no user filter; products are pre-ingested)
        product_docs: List[Document] = []
        try:
            if hasattr(self.product_vs, "similarity_search_with_relevance_scores"):
                pairs = self.product_vs.similarity_search_with_relevance_scores(
                    query, k=self.k_product
                )
                product_docs = [
                    doc for doc, score in pairs if (score or 0) >= self.min_relevance
                ]
            else:
                product_docs = self.product_vs.similarity_search(
                    query, k=self.k_product
                )
        except Exception:
            product_docs = []

        # Merge and return
        return user_docs + product_docs


@chat_bp.route("/inventory", methods=["POST"])
@jwt_required
def chat_inventory():
    """
    Answer inventory-related questions using RAG and store/cache responses.
    """
    data = request.get_json(force=True, silent=True)
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question: str = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    # Decide which LLM to use (factory driven)
    use_ollama = str(data.get("use_ollama", "false")).lower() == "true"
    provider = "ollama" if use_ollama else "openai"
    model_name = "ollama-rag" if use_ollama else "openai-rag"

    try:
        # Identify current user
        user = get_current_user()
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401

        # 1. Check cache (tenant-scoped)
        cached = get_cached_response(
            model_name=model_name, prompt=question, user_id=int(user.id)
        )
        if cached:
            return (
                jsonify({"answer": cached, "model": model_name, "cached": True}),
                200,
            )

        # 2. Build vector stores lazily (avoid env access at import time)
        product_vs = load_vector_store(collection_name="product_embeddings_hf")
        user_vs = load_vector_store(collection_name="user_embeddings_hf")

        # Build a combined retriever (user + products) and wrap as Runnable
        cr = CombinedRetriever(user_vs, product_vs, user_id=int(user.id))
        retriever = RunnableLambda(lambda q: cr.get_relevant_documents(q))
        chain = build_rag_chain(retriever, provider=provider)

        answer: str = chain.invoke(question)

        # 3. Store in cache (tenant-scoped)
        set_cached_response(
            model_name=model_name, prompt=question, response=answer, user_id=int(user.id)
        )

        return jsonify({"answer": answer, "model": model_name}), 200

    except Exception as e:
        logger.error(f"Error processing question '{question}': {str(e)}")
        return jsonify({"error": str(e)}), 500
