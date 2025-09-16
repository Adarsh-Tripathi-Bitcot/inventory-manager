import logging
import os
import psycopg2
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from week_9.api.constants import HF_EMBEDDING_MODEL
from week_9.prompts.system_prompt import RAG_PROMPT_TEMPLATE
from week_9.api.utils.llm_factory import get_llm  

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_db_connection():
    """Return a new PostgreSQL connection using DATABASE_URL."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    return psycopg2.connect(db_url)


def load_vector_store(collection_name: str = "langchain_pg_embedding") -> PGVector:
    """
    Load or create a PGVector vector store using Hugging Face embeddings.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    logger.info(f"Loading vector store from collection '{collection_name}'...")

    embeddings = HuggingFaceEmbeddings(model_name=HF_EMBEDDING_MODEL)

    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,
    )
    return vector_store


def build_rag_chain(vector_store_or_retriever, provider: str = "openai"):
    """
    Build a RAG pipeline using retriever, system prompt, and LLM.

    Args:
        vector_store_or_retriever: PGVector vector store or an already-configured retriever.
        provider (str): 'openai' or 'ollama'

    Returns:
        chain: Configured RAG chain.
    """
    # Accept three cases:
    # 1) Retriever-like (has get_relevant_documents) → wrap as RunnableLambda
    # 2) Vectorstore-like (has as_retriever) → convert
    # 3) Already a Runnable (fallback) → use directly
    if hasattr(vector_store_or_retriever, "get_relevant_documents"):
        retriever = RunnableLambda(lambda q: vector_store_or_retriever.get_relevant_documents(q))
    else:
        if hasattr(vector_store_or_retriever, "as_retriever"):
            retriever = vector_store_or_retriever.as_retriever()
        else:
            retriever = vector_store_or_retriever
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    llm = get_llm(provider=provider)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def get_or_cache_answer(rag_chain, question: str) -> str:
    """Check cache for an answer, otherwise run the chain and insert into cache."""
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT answer FROM llm_cache WHERE question = %s;", (question,))
        row = cur.fetchone()
        if row:
            logger.info("Cache hit for question: %s", question)
            return row[0]

        logger.info("Cache miss → querying LLM for: %s", question)
        answer = rag_chain.invoke(question)

        cur.execute(
            "INSERT INTO llm_cache (question, answer) VALUES (%s, %s);",
            (question, answer),
        )
        conn.commit()
        return answer
    finally:
        cur.close()
        conn.close()
