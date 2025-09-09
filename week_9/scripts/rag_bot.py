import logging
import os
import psycopg2
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector

from week_8.api.constants import (
    OPENAI_CHAT_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_EMBEDDING_MODEL,
)
from week_8.prompts.system_prompt import RAG_PROMPT_TEMPLATE

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_db_connection():
    """Return a new PostgreSQL connection using DATABASE_URL."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    return psycopg2.connect(db_url)


def load_vector_store(collection_name: str = "product_embeddings") -> PGVector:
    """Load existing PGVector embeddings from the database."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    logger.info(f"Loading vector store from collection '{collection_name}'...")
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,  # Required for similarity search
    )
    return vector_store


def build_rag_chain(vector_store: PGVector):
    """Build a RAG pipeline using retriever, system prompt, LLM, and output parser."""
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
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
