# Week 8 — LLMs, Embeddings & RAG (Inventory Chatbot)

**Goal:** Transition the inventory project to the AI stack: learn LLMs & embeddings, build a retrieval-augmented generation (RAG) pipeline, ingest product text into `pgvector`, and expose a JWT-protected `/chat/inventory` endpoint that answers natural-language questions about products.

> This README documents **only** the `week_8` work and steps to run / test the RAG-powered chat API.

---

## Index
- [Project Overview & Architecture](#project-overview--architecture)  
- [Project structure (week_8)](#project-structure-week_8)  
- [Environment & Required Config](#environment--required-config)  
- [Setup & Local Run Steps](#setup--local-run-steps)  
- [Scripts (ingest / embeddings / rag)](#scripts-ingest--embeddings--rag)  
- [API: Chat Blueprint & Endpoint](#api-chat-blueprint--endpoint)   
- [Checklist (Week 8 deliverables)](#checklist-week-8-deliverables)  

---

## Project overview & architecture

**High level:**  
- A RAG-powered inventory chatbot: product data is embedded into a persistent vector store (Postgres + `pgvector`), LangChain PGVector retriever fetches relevant product context, and a LangChain chain (LCEL) composes retriever → prompt → LLM to produce answers.  
- The chain is exposed via a new Flask blueprint: `POST /chat/inventory`. The endpoint is JWT-protected.

**Key design choices:**
- Vector store: `pgvector` extension in PostgreSQL (persistent embeddings).  
- Embeddings: OpenAI embedding model (configurable via env).  
- LLM: OpenAI Chat model via LangChain (`ChatOpenAI`).  
- Chain composition: LangChain Expression Language (LCEL) with `RunnablePassthrough` for the question.  
- Startup behavior: vector store and chain loaded once at Flask startup (to avoid rebuilding per request).  
- Ingestion scripts are separate from runtime; embeddings are generated once by scripts.

---

## Project structure (week_8) — important files

```
week_8/
├── api/
│   ├── app.py                        # Flask app factory (registers blueprints)
│   ├── config.py
│   ├── constants.py
│   ├── db.py
│   ├── models.py                     # Product, User, SentenceEmbedding (Vector column)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── products.py
│   │   └── chat.py                   # <- NEW: chat blueprint with /chat/inventory
│   └── utils/
│       └── embeddings.py             # helper for OpenAI embeddings (ingest)
├── prompts/
│   ├── system_prompt.py 
├── scripts/
│   ├── data_loader.py                # loads product data for ingestion
│   ├── embed_sentences.py            # generate embeddings for chunks & write to DB
│   ├── ingest_embeddings.py          # wrapper that calls embedding ingestion
│   └── rag_bot.py                    # build_rag_chain() and load_vector_store()
└── migrations/                        # alembic migrations, includes sentence_embeddings
```

## Environment & required config (examples)

- Set these in your .env or environment before running:
```
    DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
    OPENAI_API_KEY=sk-...
    OPENAI_CHAT_MODEL=gpt-4o-mini      # or gpt-3.5-turbo, etc (configurable)
    OPENAI_EMBEDDING_MODEL=text-embedding-3-small
    OPENAI_TEMPERATURE=0.0
    JWT_SECRET_KEY=supersecret
```

- week_8/api/constants.py contains model/embedding name constants used by scripts and rag_bot.

## Setup & local run steps

- Create & activate virtualenv, install dependencies (existing requirements.txt):
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Ensure PostgreSQL is running and pgvector extension is enabled on your DB. (If using Docker, enable pgvector in the container.)

- Run migrations:
```
export FLASK_APP=week_8.api.app:create_app
flask db upgrade
```

- Ingest product text & embeddings (run ingestion scripts once):
- Generate text chunks and embeddings, store into sentence_embeddings table
```
python -m week_8.scripts.embed_sentences
python -m week_8.scripts.ingest_embeddings
```
- Run  rag-cahin using command
```
python -m week_8.scripts.rag_bot
```

- Start the Flask app:
```
export FLASK_APP=api.app:create_app
flask run
```


## Scripts (ingest / embeddings / rag)

- scripts/data_loader.py
- Loads product rows and generates product text (name + generated description) for embedding.

- scripts/embed_sentences.py
- Splits product text into chunks (if needed), calls OpenAI embeddings via api/utils/embeddings.py, and writes rows into sentence_embeddings (Vector column).

- scripts/ingest_embeddings.py
- Wrapper orchestration script that combines data load + embedding + DB write.

- scripts/rag_bot.py
```
load_vector_store(collection_name: str = "product_embeddings") — returns a PGVector instance connected to the DB.

build_rag_chain(vector_store: PGVector) — constructs the LCEL chain:

{"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
```

- main() — example invocation (not used by the API).

- Note: week_8/api/utils/embeddings.py contains the OpenAI client helper used by embed scripts.


## API: Chat blueprint & endpoint

- Blueprint: week_8/api/routes/chat.py
- Endpoint: POST /chat/inventory (url prefix /chat)

- Request
```
{
  "question": "Which products are low on stock?"
}
```

- Response
```
{
  "answer": "The LLM's answer ..."
}
```


## Checklist — Week 8 deliverables (completed)

- Create DB table with Vector column (sentence_embeddings).

- Script(s) to ingest product info and store embeddings.

- Use LangChain to build RAG chain (PGVector retriever → prompt → LLM).

- Prompt designed to constrain model to provided context.

- Add chat blueprint to Flask app.

- Add POST /chat/inventory endpoint accepting {"question": "..."}.

- Endpoint protected by @jwt_required.

- Endpoint executes RAG chain and returns JSON answer.

- PR created and tested locally.