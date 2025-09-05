# Project Architecture

## Overview
The **Inventory Manager** project follows a progressive design:
1. Week 2 – Procedural script.
2. Week 3 – Object-Oriented, modular package.
3. Week 4 – Test-driven development with high coverage.
4. Week 5 – RESTful API using Flask.
5. Week 6 – Flask API integrated with PostgreSQL for persistent storage.
6. Week 7 – Focuses on implementing **authentication, authorization, and role-based access control** for the Flask API
---

## Folder Structure
```
inventory-manager/
├── docs
│   ├── ARCHITECTURE.md
│   ├── INDEX.md
│   ├── SETUP.md
│   └── TESTING.md
├── errors.log
├── low_stock_report.txt
├── pytest.ini
├── README.md
├── week_1
│   ├── f_principle.py
│   └── practice.py
├── week_2
│   ├── control_flow.py
│   ├── csv_utils.py
│   ├── daily_drills.py
│   ├── dictionary_utils.py
│   ├── error_handling.py
│   ├── errors.log
│   ├── file_handling.py
│   ├── function_utils.py
│   ├── inventory.csv
│   ├── items.csv
│   ├── list_utils.py
│   ├── low_stock_report.txt
│   ├── process_inventory.py
│   ├── pydantic_utils.py
│   ├── requirements.txt
│   ├── sample.csv
│   ├── sample.txt
│   ├── set_utils.py
│   ├── tuple_utils.py
├── week_3
│   ├── data
│   │   └── products.csv
│   ├── errors.log
│   ├── inventory_manager
│   │   ├── core.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── utils.py
│   ├── low_stock_report.txt
│   ├── main.py
│   ├── pyproject.toml
│   ├── requirements.txt
├── week_4
│   └── tests
│       ├── conftest.py
│       ├── errors.log
│       ├── __pycache__
│       ├── requirements.txt
│       ├── test_core.py
│       ├── test_models_fixture.py
│       ├── test_models.py
│       └── venv
├── week_5
│   ├── api
│   │   ├── app.py
│   │   ├── __init__.py
│   │   └── routes
│   ├── Day_1
│   │   └── hello.py
│   ├── requirements.txt
│   ├── tests
│   │   └── test_api_integration.py
└── week_6_and_7
    ├── api
      │   ├── app.py
      │   ├── config.py
      │   ├── db.py
      │   ├── __init__.py
      │   ├── models.py
      │   ├── request_model.py
      │   ├── response_model.py
      │   ├── routes
      │   │   ├── auth_routes.py
      │   │   ├── __init__.py
      │   │   ├── products.py
      │   ├── schemas.py
      │   ├── seed.py
      │   └── utils
      │       ├── __init__.py
      │       └── security.py
   ├── data
   │   └── products.csv
   ├── errors.log
   ├── __init__.py
   ├── migrations
   │   ├── alembic.ini
   │   ├── env.py
   │   ├── README
   │   ├── script.py.mako
   │   └── versions
   ├── requirements.txt
   ├── tests
   │   ├── conftest.py
   │   ├── __init__.py
   │   ├── test_app.py
   │   ├── test_config.py
   │   ├── test_models.py
   │   ├── test_request_response_models.py
   │   ├── test_routes.py
   │   ├── test_security.py
   │   └── test_seed.py
week_8/
├── api/
│   ├── app.py                        
│   ├── config.py
│   ├── constants.py
│   ├── db.py
│   ├── models.py                    
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── products.py
│   │   └── chat.py             
│   └── utils/
│       └── embeddings.py             
├── scripts/
│   ├── data_loader.py               
│   ├── embed_sentences.py          
│   ├── ingest_embeddings.py         
│   └── rag_bot.py                
└── migrations/                       
```



## Core Components

### 1. `models.py`
- Defines `Product` class using **Pydantic** for type safety & validation.
- Ensures:
  - `quantity` ≥ 0
  - `price` > 0

### 2. `core.py`
- Contains `Inventory` class.
- Responsibilities:
  - Load data from CSV
  - Add/remove products
  - Generate low-stock reports
  - Calculate total inventory value

### 3. `utils.py`
- Logging helpers for validation errors.
- Error log file: `errors.log`.

### 4. `data/`
- Contains sample CSV files for development and testing.

---

## Data Flow
1. **CSV Load** → `Inventory.load_from_csv()`  
2. **Validation** → `Product` model (Pydantic)  
3. **Processing** → Inventory operations (add, remove, report)  
4. **Output** → Text/CSV reports + logs

---

## Design Principles
- **SRP (Single Responsibility Principle)** – each module does one thing well.
- **OCP (Open/Closed Principle)** – extend with new features without modifying existing code.
- **Loose Coupling** – `models` independent from `utils`.
- **Testability** – functions accept dependencies as parameters for easy mocking.


## Week 5 – API Architecture

### New Components
1. **`week_5/api/app.py`**
   - Flask application entry point.
   - Registers the `api` blueprint.

2. **`week_5/api/routes/products.py`**
   - Contains CRUD routes for products.
   - Uses `inventory_manager` package as the business logic.

3. **`week_5/tests/test_api_integration.py`**
   - Integration tests for all API endpoints.

---

### API Data Flow
1. **HTTP Request** → Flask route in `products.py`
2. **Validation** → Pydantic `Product` model
3. **Processing** → `Inventory` class from `inventory_manager`
4. **HTTP Response** → JSON with proper status code


# Project Architecture – Week 6 and 7

## Overview
Week 7 of the **Inventory Manager** project focuses on implementing **authentication, authorization, and role-based access control** for the Flask API.  
Key highlights:
1. JWT-based authentication for secure access.
2. Role-based restrictions (e.g., manager vs. staff).
3. Integration with existing CRUD endpoints.
4. Test coverage for security-related functionality.

---

---

## Core Components

### 1. `auth_routes.py`
- Handles **user registration and login**.
- Generates **JWT access tokens** for authenticated users.
- Supports **role-based access control**:
  - `manager` can create/update products.
  - `staff` can only view products.

### 2. `security.py`
- Password hashing using `bcrypt`.
- JWT token encoding and decoding.
- Token validation and expiration checks.

### 3. `models.py`
- Adds `User` model with `username`, `password_hash`, and `role`.
- Maintains relationship with existing `Product` model.

### 4. `request_model.py` & `response_model.py`
- Pydantic schemas for authentication requests and responses.
- Ensures proper validation for login/register payloads.

---

## Data Flow

1. **Registration** → User credentials validated → Password hashed → Saved in DB
2. **Login** → Credentials verified → JWT token issued
3. **JWT Token Usage** → Included in `Authorization: Bearer <token>` header for protected routes
4. **Role Checks** → Endpoint verifies `role` from token → Allows or denies action
5. **CRUD Operations** → Processed only if authorization passes

---

## Design Principles

- **Security First** – Password hashing, JWT, role-based access.
- **SRP & OCP** – Each module handles a single responsibility and can be extended without modification.
- **Loose Coupling** – Security logic in `utils/security.py` independent from routes.
- **Testable** – Routes, security utils, and DB operations are unit-tested and mockable.


# Project Architecture – Week 8

**Goal:** Transition the inventory project to the AI stack: learn LLMs & embeddings, build a retrieval-augmented generation (RAG) pipeline, ingest product text into `pgvector`, and expose a JWT-protected `/chat/inventory` endpoint that answers natural-language questions about products.

---

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

## Index
- [Project Overview & Architecture](#project-overview--architecture)  
- [Project structure (week_8)](#project-structure-week_8)  
- [Environment & Required Config](#environment--required-config)  
- [Setup & Local Run Steps](#setup--local-run-steps)  
- [Scripts (ingest / embeddings / rag)](#scripts-ingest--embeddings--rag)  
- [API: Chat Blueprint & Endpoint](#api-chat-blueprint--endpoint)   
- [Checklist (Week 8 deliverables)](#checklist-week-8-deliverables)  

---