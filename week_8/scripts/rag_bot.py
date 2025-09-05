# week_8/scripts/rag_bot.py
import logging
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings

# from week_8.scripts.data_loader import load_products
from week_8.api.constants import OPENAI_CHAT_MODEL, OPENAI_TEMPERATURE, OPENAI_EMBEDDING_MODEL

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_vector_store(collection_name: str = "product_embeddings") -> PGVector:
    """
    Load existing PGVector embeddings from the database.
    """
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
    """
    Build a simple RAG pipeline: retriever → prompt → LLM → output parser
    """
    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use the provided product context to answer the user's question.",
            ),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ]
    )

    llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=OPENAI_TEMPERATURE)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def main():
    # Do NOT generate embeddings here anymore
    logger.info("Loading existing embeddings from vector DB...")
    vector_store = load_vector_store()

    logger.info("Building RAG chain...")
    rag_chain = build_rag_chain(vector_store)

    # Example query
    question = "Quantity of onion?"
    logger.info(f"Asking RAG chain: {question}")
    answer = rag_chain.invoke(question)

    print("\n=== RAG Answer ===")
    print(answer)


if __name__ == "__main__":
    main()
