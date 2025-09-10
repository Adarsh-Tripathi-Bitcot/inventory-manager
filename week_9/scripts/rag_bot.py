import logging
import os
import psycopg2
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from week_9.api.constants import (
    OPENAI_CHAT_MODEL,
    OPENAI_TEMPERATURE,
)
from week_9.prompts.system_prompt import RAG_PROMPT_TEMPLATE

from week_9.api.constants import (
    HF_EMBEDDING_MODEL,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
)

from week_9.api.utils.ollama_llm import get_ollama_llm
from langchain_openai import ChatOpenAI

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

    Args:
        collection_name (str): Name of the PGVector collection.

    Returns:
        PGVector: Vector store object.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    logger.info(f"Loading vector store from collection '{collection_name}'...")

    embeddings = HuggingFaceEmbeddings(model_name=HF_EMBEDDING_MODEL)

    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,  # Required for similarity search
    )

    return vector_store


def build_rag_chain(vector_store: PGVector, use_ollama: bool = False):
    """
    Build a RAG pipeline using retriever, system prompt, and LLM.

    Args:
        vector_store (PGVector): Vector store for retrieval.
        use_ollama (bool): If True, use Ollama LLM instead of OpenAI.

    Returns:
        chain: Configured RAG chain.
    """
    # Retriever
    retriever = vector_store.as_retriever()

    # Prompt
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

    # Choose LLM
    if use_ollama:
        logger.info("Using Ollama model for RAG pipeline...")
        llm = get_ollama_llm(model=OLLAMA_MODEL, temperature=OLLAMA_TEMPERATURE)
    else:
        logger.info("Using OpenAI model for RAG pipeline...")
        llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=OPENAI_TEMPERATURE)

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
        # 1. Check cache
        cur.execute("SELECT answer FROM llm_cache WHERE question = %s;", (question,))
        row = cur.fetchone()
        if row:
            logger.info("Cache hit for question: %s", question)
            return row[0]

        # 2. Not cached → run chain
        logger.info("Cache miss → querying LLM for: %s", question)
        answer = rag_chain.invoke(question)

        # 3. Insert into cache
        cur.execute(
            "INSERT INTO llm_cache (question, answer) VALUES (%s, %s);",
            (question, answer),
        )
        conn.commit()
        return answer
    finally:
        cur.close()
        conn.close()
