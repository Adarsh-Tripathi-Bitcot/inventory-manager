## `README.md`


# Inventory Manager

A Python-based inventory management tool built as a **6-week learning project**, evolving from basic scripts to a fully tested, object-oriented package.


## Features
- Process CSV inventory files
- Validate product data with Pydantic
- Generate low-stock reports
- Calculate total inventory value
- RESTful Flask API for inventory management
- PostgreSQL database integration
- CRUD operations for products
- Request/response validation with Pydantic
- Seed scripts for initial DB population
- Full test suite with >95% coverage including API endpoints
- JWT-based authentication
- Role-based authorization (manager/staff)
- Secure CRUD operations for products
- Implemented RAG-based chat system with PostgreSQL vector store (PGVector) for multi-tenant document retrieval.
- Added OpenAI vs. Ollama integration — switchable via use_ollama flag to run locally or in the cloud.
- Enhanced Flask API endpoints (/chat/inventory, /api/documents/upload) with JWT authentication and caching for tenant-scoped responses.


## Learning Journey
- **[Week 1–9 Overview](docs/INDEX.md)**
- **[Architecture](docs/ARCHITECTURE.md)**
- **[Setup & Installation](docs/SETUP.md)**
- **[Testing Guide](docs/TESTING.md)**



## Project Structure
```
inventory-manager/
├── week_1/
├── week_2/
├── week_3/
├── week_5/
├── tests/
├── week_6_and_7/
├── week_8/
├── week_9/
├── requirements.txt
├── pytest.ini
└── README.md
```