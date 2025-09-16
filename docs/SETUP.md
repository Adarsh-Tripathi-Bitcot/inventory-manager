# Setup & Installation

## Requirements
- Python 3.10+
- [Pydantic v2](https://docs.pydantic.dev)
- pytest, pytest-mock, pytest-cov (for tests)
- Black & Ruff (for formatting and linting)
- Flask
- SQLAlchemy
- Alembic (for migrations)
- psycopg2-binary (PostgreSQL driver)
- 

---

## 1. Clone the Repository
```bash
git clone <your-repo-url>
cd inventory-manager

2. Create and Activate a Virtual Environment
Linux/macOS:
python -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate


3. Install Dependencies
pip install -r requirements.txt


4. Run the Application
Procedural (Week 2 version):
cd week_2
python process_inventory.py


OOP (Week 3 version):
python main.py


5. Run Tests
pytest
With coverage report:
pytest --cov=.



## Running the Flask API (Week 5)

1. Activate virtual environment:
```bash
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


2. Install dependencies:
pip install -r requirements.txt


3. Run the Flask API:
cd week_5/api
python -m week_5.api.app


API will be available at:

http://127.0.0.1:5000/api/products



## Running the Flask + PostgreSQL API (Week 6)

1. Activate virtual environment:
```bash
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


2. Install dependencies:
pip install -r requirements.txt


3. Run the Flask API:
cd week_5/api

4. Run the development server
export FLASK_APP=api.app:create_app
flask run 

5. Initialize migrations & create schema
flask db init      # only the first time
flask db migrate -m 
flask db upgrade

6. Seed the DB from data/products.csv
flask seed-db
# will print summary and write invalid rows to errors.log

API will be available at:

http://127.0.0.1:5000/api/products



# Setup & Installation – Week 7

## Requirements
- Python 3.10+
- Flask
- SQLAlchemy
- Alembic
- psycopg2-binary
- Pydantic v2
- bcrypt
- Pytest, pytest-mock, pytest-cov
- Black & Ruff

---

## 1. Clone the Repository
```bash
git clone <your-repo-url>
cd inventory-manager

## 2. Create and Activate Virtual Environment

Linux/macOS:

python -m venv venv
source venv/bin/activate


Windows:

python -m venv venv
venv\Scripts\activate

## 3. Install Dependencies
pip install -r requirements.txt

## 4. Run Flask + PostgreSQL API (Week 7)
export FLASK_APP=api.app:create_app
flask run

## 5. Initialize Database
flask db init       # first time only
flask db migrate -m "Initial migration with User table"
flask db upgrade

## 6. Seed Data
flask seed-db

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



# Setup Guide – Week 9

## 1. Clone & Enter Project
```bash
git clone <your-repo-url>
cd inventory-manager/week_9


## 2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

## 3. Install Dependencies
pip install -r requirements.txt


## 4. Environment Variables
DATABASE_URL=postgresql://user:pass@localhost/db_name
OPENAI_API_KEY=sk-...
MODEL_BACKEND=openai    
CACHE_TTL=3600          
JWT_SECRET=supersecret


## 5. Database Migrations
flask db upgrade

## 6. Embedding Ingestion
python -m week_9.scripts.ingest_embeddings


## 7.1 Install & Run Ollama
curl -fsSL https://ollama.com/install.sh | sh

## 7.2 Pull a Model
ollama pull llama3


## 7.3 Test Locally
ollama run llama3 "Hello, how are you?"


## 8. Run the App
flask run 

## 9. Using Ollama with the Chat Endpoint
curl -X POST http://127.0.0.1:5000/chat/inventory \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your-JWT>" \
-d '{
  "question": "Summarize the uploaded product documents.",
  "use_ollama": true
}'

## 10. Upload & Chat Workflow

POST /documents/upload (JWT required) to upload a file.
POST /chat/inventory (JWT required) to ask a question.
Add "use_ollama": true in the JSON to switch to the local model.