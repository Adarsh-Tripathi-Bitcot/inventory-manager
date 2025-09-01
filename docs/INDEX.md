## Overview Week - 1

# Inventory Manager

A beginner-friendly Python project to practice Git workflows, environment setup, and core Python programming concepts, including data structures, procedural programming, error handling, and data validation using Pydantic.

---

## Python Concepts Practiced

- Virtual environments (`venv`)
- The Zen of Python (`import this`)
- List comprehensions vs. for loops
- Equality (`==`) vs. identity (`is`)
- Git branching: `main` → `develop` → `feature/week_1`, `feature/week_2`
- Pull Request (PR) workflow for team collaboration


## Overview Week - 2

This week focused on mastering core Python data structures and procedural programming techniques, culminating in a real-world command-line tool to process inventory data from a CSV file.

---

## Project Structure
```
inventory-manager/
├── .gitignore
├── README.md
├── week_1/
│   ├── f_principle.py
│   ├── practice.py
│   └── venv/  (not tracked)
├── week_2/
│   ├── control_flow.py
│   ├── csv_utils.py
│   ├── daily_drills.py
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
│   ├── sample.csv
│   ├── sample.txt
│   ├── set_utils.py
│   ├── tuple_utils.py
│   └── venv/  (not tracked)

---

## How to Set Up & Run

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd inventory-manager

# Navigate to week_2 folder
cd week_2

# Create virtual environment
python3 -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# (On Windows)
venv\Scripts\activate

# 3. Install Dependencies
pip install pydantic


# How to Run the Project
python process_inventory.py
```

## Daily Topics & Learnings

### Day 1: Lists & Tuples

- **Lists**: Creation, indexing, slicing, appending, and removing elements.
  - Common methods: `.append()`, `.extend()`, `.pop()`, `.sort()`
- **Tuples**: Syntax, immutability, and use-cases.
- **Key Distinction**:
  - Use **lists** for homogeneous, mutable collections.
  - Use **tuples** for heterogeneous, fixed data (e.g., return multiple values from a function).

---

### Day 2: Dictionaries & Sets

- **Dictionaries**: Key-value pairs, creation, accessing, updating.
  - Iteration with `.keys()`, `.values()`, `.items()`
- **Sets**: Unordered collections of unique items.
  - Use cases: duplicate removal, fast membership testing.
  - **Performance**:
    - Lookup in set: **O(1)**
    - Lookup in list: **O(n)**

---

### Day 3: Control Flow & Functions

- **Control Flow**: `if`, `elif`, `else`, `for`, `while`
- **Functions**:
  - Parameters and return values
  - Applied **Single Responsibility Principle (SRP)**:
    - Each function does one thing well
  - Used procedural decomposition for code clarity

---

### Day 4: File I/O & `csv` Module

- **File Handling**: Using `with open(...) as f:` for reading/writing plain text
- **CSV Handling**:
  - `csv.reader`: Basic row parsing
  - `csv.DictReader`: Structured row parsing using headers
- **CSV Pitfalls**: Manual parsing fails with commas in quoted fields

---

### Day 5: Error Handling & Data Validation with Pydantic

- **Error Handling**:
  - `try...except`
  - Specific exceptions: `FileNotFoundError`, `ValueError`, `ValidationError`
- **Pydantic**:
  - Defined `Product` model with type validations:
    - `quantity`: non-negative `int`
    - `price`: positive `float`
  - Caught validation issues and logged errors instead of crashing

---

## Daily Drills

1. **Remove duplicates from a list** using `set()`
2. **Convert list of tuples into a dictionary**:
   ```python
   dict([("Alice", 80), ("Bob", 90)])


# Inventory Manager – Week 3

A continuation of the inventory processor project, this week applies **Object-Oriented Programming (OOP)** principles and project structuring best practices. The goal is to transform procedural code into a clean, modular, and extensible Python package.

---

## Overview – Week 3

This week focused on understanding and applying Object-Oriented Programming (OOP) concepts to refactor the inventory tool built in Week 2. By organizing code into classes and separating concerns, the project becomes easier to maintain, test, and extend.

---

## Project Structure for Week-3 (OOP Version)

```
week_3/
  inventory-manager/
  ├── init.py           # Marks the directory as a package
  ├── models.py         # Pydantic Product model & subclasses
  ├── core.py           # Inventory class (business logic)
  ├── utils.py          # Logging helpers (e.g., for validation errors)
  ├── data/
  │ └── products.csv    # Inventory data file
  │
  ├── errors.log                  # Auto-generated log for validation issues
  ├── low_stock_report.txt        # Auto-generated report for low stock items
  ├── main.py                     # To Run the Project
  ├── pyproject.toml              # Black + Ruff configuration
  ├── requirements.txt            # Pydantic, Black, Ruff

  ```

## How to Set Up & Run

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd inventory-manager

# 2. Set Up Virtual Environment
virtualenv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Install Dependencies
pip install -r requirements.txt

# How to Run the Project
python main.py
```

Key Concepts Practiced
```
Object-Oriented Programming (OOP)

SRP & OCP principles (Clean Code)

Data validation with Pydantic

Modular Python package design

Code quality tools: Black and Ruff
```

🧪 Tools Used
```
| Tool         | Purpose                      |
| ------------ | ---------------------------- |
| **Pydantic** | Validation of product data   |
| **Black**    | Auto formatting              |
| **Ruff**     | Fast and configurable linter |
```

Run them like this:
```
black .
ruff .
```


# Week 4 – Test-Driven Development (TDD) with Pytest

[![Coverage Status](https://img.shields.io/badge/coverage-97%25-brightgreen)](https://pytest-cov.readthedocs.io/)

## Overview
This week’s goal was to build strong **Test-Driven Development (TDD)** skills using **pytest**.  
The focus was on:
- Writing tests before implementation (**Red-Green-Refactor** cycle)
- Using fixtures to avoid repeated setup
- Mocking and patching to test code with external dependencies (e.g., file system) without touching real files
- Parameterizing tests to check multiple scenarios efficiently
- Measuring code coverage and understanding its limitations

By the end of the week, I developed a **comprehensive test suite** for the `inventory_manager` package that covers core functionalities of the `Product` and `Inventory` classes.

---

## Project Structure
```
inventory-manager/
│
├── week_3/
│ └── inventory_manager/
│ ├── init.py
│ ├── core.py # Inventory class and business logic
│ ├── models.py # Product subclasses with Pydantic validation
│ └── utils.py
│
├── tests/
│ ├── conftest.py # Shared pytest fixtures
│ ├── test_core.py # Tests for core Inventory logic
│ ├── test_models.py # Tests for Product models with parametrization
│ ├── test_models_fixture.py # Fixture-based model tests with parametrization
│ └── test_inventory.py # TDD for get_inventory_value method
│
├── pytest.ini # Pytest configuration
└── requirements.txt # Dependencies
```


## ⚙️ How to Set Up & Run

### 1. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

2. Install dependencies
pip install -r requirements.txt


3. Run tests
pytest


4. Run tests with coverage report
pytest --cov=.
```

## Key Concepts Practiced

### 1. TDD (Test-Driven Development)
**Red–Green–Refactor** approach:
- **Red**: Write a failing test  
- **Green**: Write just enough code to make it pass  
- **Refactor**: Improve code while keeping tests passing  

### 2. Pytest Fixtures
- Created reusable test data (`base_product`, `inventory`, etc.)  
- Reduced repetitive setup code across multiple tests  

### 3. Mocking & Patching
- Used `pytest-mock` to replace:
  - `open()` calls in `load_from_csv` to avoid touching real files  
  - File writing in `generate_low_stock_report`  

### 4. Parametrization
- Applied `@pytest.mark.parametrize` to test multiple inputs in a single function  
- Reduced code duplication in validation error tests  

### 5. Coverage Analysis
- Used `pytest-cov` to measure test coverage  
- Achieved **>95% coverage** for the `inventory_manager` package  

---

## Tools Used
- **Python 3.10+**
- `pytest` – Test framework  
- `pytest-mock` – Mocking/patching support  
- `pytest-cov` – Coverage reporting  
- `pydantic` – Model validation  
- `unittest.mock` – For mocking built-in functions  

---

## End-of-Week Achievements
- Built a full-featured **test suite** for `inventory_manager`  
- Practiced **TDD** by adding a new `get_inventory_value()` method  
- Implemented **mock-based tests** for file I/O without touching disk  
- Improved tests using **parametrization**  
- Achieved **high test coverage** with meaningful assertions  




# Overview – Week 5

# Inventory Manager – Web API with Flask

A continuation of the Inventory Manager project, this week focuses on exposing our inventory functionality as a **RESTful web API** using the **Flask** framework.

---

## Goals
- Understand HTTP fundamentals and REST API principles.
- Use Flask Blueprints to structure API endpoints.
- Implement **CRUD** operations:
  - Create (`POST`)
  - Read (`GET`)
  - Update (`PUT`)
- Validate request data using **Pydantic**.
- Write **integration tests** with pytest and Flask’s test client.

---

## Daily Breakdown

### Day 1 – Intro to APIs & Flask
- Learned the request–response cycle and key HTTP verbs.
- Built a minimal `Hello, World!` Flask app.
- Tested using Postman / Thunder Client.

### Day 2 – Project Structure with Blueprints
- Avoided a monolithic `app.py` by introducing **Blueprints**.
- Created an `api` blueprint for product endpoints.
- Integrated the existing **inventory_manager** package as the business logic layer.

### Day 3 – Read Endpoints
- `GET /api/products` → List all products (JSON).
- `GET /api/products/<product_id>` → Single product details or `404`.

### Day 4 – Create & Update Endpoints
- `POST /api/products` → Validate JSON body, create product, return `201`.
- `PUT /api/products/<product_id>` → Validate JSON body, update product.

### Day 5 – Integration Testing

[![Coverage Status](https://img.shields.io/badge/coverage-98%25-brightgreen)](https://pytest-cov.readthedocs.io/)

- Configured **Flask test client** for pytest.
- Wrote request-based tests for all CRUD endpoints in `week_5/tests/test_api_integration.py`.

---

## Project Structure (Week-5)
```
week_5/
├── api/
│ ├── init.py
│ ├── app.py # Flask app factory
│ └── routes/
│ ├── init.py
│ └── products.py # CRUD endpoints
├── tests/
│ └── test_api_integration.py
└── Day_1/
└── hello.py # Initial Hello World app
```

## Key Learnings
- How a REST API differs from a traditional web app.
- Proper use of HTTP verbs and status codes.
- Benefits of Flask Blueprints for modularity.
- Difference between **unit tests** and **integration tests**.

---

## End-of-Week Achievements
- Functional Flask API with CRUD endpoints.
- Validation integrated using Pydantic.
- Integration test coverage for all routes.
- Clean, modular API design following REST best practices.


# Overview - Week 6

# Week 6: Persistent Data with SQLAlchemy and PostgreSQL
This week focuses on integrating PostgreSQL with the existing Flask API. The goal was to replace CSV-based storage with a relational database, implement proper CRUD operations, and ensure seamless interaction between Flask routes and the PostgreSQL backend.


## Goals
- Integrate Flask API with PostgreSQL using SQLAlchemy.
- Validate requests and responses using Pydantic models.
- Seed DB with CSV without interfering with production data.
- Implement integration tests for all endpoints.
- Learn mocking, patching, and test coverage with pytest.

## Project Structure (Week-6)
```
week_6/
├── api/
│   ├── __init__.py       # Flask app factory + DB initialization
│   ├── app.py            # Entry point to run the API
│   ├── config.py         # Config classes (Dev, Test, Prod)
│   ├── db.py             # PostgreSQL connection setup
│   ├── models.py         # SQLAlchemy models
│   ├── request_model.py  # Pydantic request schemas
│   ├── response_model.py # Pydantic response schemas
│   ├── schemas.py
│   ├── seed.py
│   └── routes/
│       ├── __init__.py
│       └── products.py   # CRUD endpoints for products
│   └── __pycache__/
│   └── data/
│       └── products.csv
│   └── migrations/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_config.py
│   ├── test_models.py
│   ├── test_request_response_models.py
│   ├── test_routes.py
│   └── test_seed.py
├── __init__.py
├── .env
├── .env.example
├── requirements.txt
```



## Key Concepts Practiced
- Setting up PostgreSQL locally and creating databases & tables
- Connecting Flask to PostgreSQL using psycopg2 / SQLAlchemy
- Implementing CRUD endpoints with database integration
- Reading environment variables for DB credentials
- Using Flask app context and connection pooling
- Writing integration tests against PostgreSQL (without touching production data)
- Ensuring proper HTTP response codes for API endpoints

## Daily Topics & Learnings
### Day 1 – PostgreSQL Setup & Database Connection
- Installed PostgreSQL and created local database
- Configured Flask to read DB credentials from environment variables
- Tested DB connection using Python scripts

### Day 2 – SQLAlchemy Models & Pydantic Schemas
- Defined SQLAlchemy models for products
- Created Pydantic request and response schemas
- Learned mapping between relational tables and Python objects

### Day 3 – CRUD Endpoints Integration
- Implemented GET, POST, PUT routes connected to PostgreSQL
- Handled proper response codes: 200, 201, 404
- Added exception handling for DB errors

### Day 4 – Integration Testing
- Configured test database (separate from dev DB)
- Wrote tests using Flask test client
- Ensured data isolation between tests
- Verified all endpoints return correct status codes and responses

### Day 5 – Refactoring & Code Quality
- Ensured consistent coding style (Black + Ruff)
- Applied type hints and docstrings for clarity
- Ensured test coverage for all API routes >95%


## End-of-Week Achievements
- Fully functional Flask API with PostgreSQL backend
- CRUD endpoints tested and validated with proper HTTP responses
- Environment-based configuration for DB credentials
- Integration tests covering all routes using Flask test client
- Clean, modular, and production-ready code structure



# Overview – Week 7

# Inventory Manager – Authentication & Security

Week 7 extends the Flask API with **secure authentication and role-based access control**.

---

## Goals
- Implement **JWT authentication** for API endpoints.
- Add **role-based access control** (manager/staff).
- Secure product CRUD operations.
- Write tests to cover **security functionality**.

---

## Key Concepts Practiced
- JWT encoding, decoding, and verification.
- Password hashing with `bcrypt`.
- Role-based access control logic.
- Secure API endpoint implementation.
- Testing login, token validation, and role restrictions.


## Project Structure (Week-7)
```
└── week_6_and_7
    ├── api
      │   ├── app.py
      │   ├── config.py
      │   ├── db.py
      │   ├── __init__.py
      │   ├── models.py
      │   ├── __pycache__
      │   ├── request_model.py
      │   ├── response_model.py
      │   ├── routes
      │   │   ├── auth_routes.py
      │   │   ├── __init__.py
      │   │   ├── products.py
      │   │   └── __pycache__
      │   ├── schemas.py
      │   ├── seed.py
      │   └── utils
      │       ├── __init__.py
      │       ├── __pycache__
      │       └── security.py
   ├── data
   │   └── products.csv
   ├── errors.log
   ├── __init__.py
   ├── migrations
   │   ├── alembic.ini
   │   ├── env.py
   │   ├── __pycache__
   │   │   └── env.cpython-310.pyc
   │   ├── README
   │   ├── script.py.mako
   │   └── versions
   │       └── __pycache__
   ├── __pycache__
   │   └── __init__.cpython-310.pyc
   ├── requirements.txt
   ├── tests
   │   ├── conftest.py
   │   ├── __init__.py
   │   ├── __pycache__
   │   ├── test_app.py
   │   ├── test_config.py
   │   ├── test_models.py
   │   ├── test_request_response_models.py
   │   ├── test_routes.py
   │   ├── test_security.py
   │   └── test_seed.py
  ```