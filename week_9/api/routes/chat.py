# from flask import Blueprint, request, jsonify
# from ..utils.security import jwt_required
# from week_9.scripts.rag_bot import load_vector_store, build_rag_chain
# from ..utils.cache import get_cached_response, set_cached_response
# import logging

# logger = logging.getLogger(__name__)

# chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# # Load vector store once
# _vector_store = load_vector_store(collection_name="product_embeddings_hf")

# # Prebuild default OpenAI chain
# _openai_chain = build_rag_chain(_vector_store, use_ollama=False)


# @chat_bp.route("/inventory", methods=["POST"])
# @jwt_required
# def chat_inventory():
#     """
#     Answer inventory-related questions using RAG and store/cache responses.

#     Request JSON:
#     {
#         "question": "Price of strawberries",
#         "use_ollama": "true"   # optional; defaults to OpenAI if not provided
#     }
#     """
#     data = request.get_json(force=True, silent=True)
#     if not data or "question" not in data:
#         return jsonify({"error": "Missing 'question' in request body"}), 400

#     question: str = data["question"].strip()
#     if not question:
#         return jsonify({"error": "Question cannot be empty"}), 400

#     # Decide which LLM to use
#     use_ollama = str(data.get("use_ollama", "false")).lower() == "true"
#     model_name = "ollama-rag" if use_ollama else "openai-rag"

#     try:
#         # 1. Check cache
#         cached = get_cached_response(model_name=model_name, prompt=question)
#         if cached:
#             return jsonify({"answer": cached, "model": model_name}), 200

#         # 2. Build and run the appropriate chain
#         if use_ollama:
#             chain = build_rag_chain(_vector_store, use_ollama=True)
#         else:
#             chain = _openai_chain

#         answer: str = chain.invoke(question)

#         # 3. Store in cache
#         set_cached_response(model_name=model_name, prompt=question, response=answer)

#         return jsonify({"answer": answer, "model": model_name}), 200

#     except Exception as e:
#         logger.error(f"Error processing question '{question}': {str(e)}")
#         return jsonify({"error": str(e)}), 500



from flask import Blueprint, request, jsonify
from ..utils.security import jwt_required
from week_9.scripts.rag_bot import load_vector_store, build_rag_chain
from ..utils.cache import get_cached_response, set_cached_response
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# Load vector store once
_vector_store = load_vector_store(collection_name="product_embeddings_hf")

# Prebuild chains at startup
_openai_chain = build_rag_chain(_vector_store, use_ollama=False)
_ollama_chain = build_rag_chain(_vector_store, use_ollama=True)


@chat_bp.route("/inventory", methods=["POST"])
@jwt_required
def chat_inventory():
    """
    Answer inventory-related questions using RAG and store/cache responses.

    Request JSON:
    {
        "question": "Price of strawberries",
        "use_ollama": "true"   # optional; defaults to OpenAI if not provided
    }
    """
    data = request.get_json(force=True, silent=True)
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question: str = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    # Decide which LLM to use
    use_ollama = str(data.get("use_ollama", "false")).lower() == "true"
    model_name = "ollama-rag" if use_ollama else "openai-rag"

    try:
        # 1. Check cache
        cached = get_cached_response(model_name=model_name, prompt=question)
        if cached:
            return jsonify({"answer": cached, "model": model_name}), 200

        # 2. Use preloaded chain
        chain = _ollama_chain if use_ollama else _openai_chain

        answer: str = chain.invoke(question)

        # 3. Store in cache
        set_cached_response(model_name=model_name, prompt=question, response=answer)

        return jsonify({"answer": answer, "model": model_name}), 200

    except Exception as e:
        logger.error(f"Error processing question '{question}': {str(e)}")
        return jsonify({"error": str(e)}), 500
