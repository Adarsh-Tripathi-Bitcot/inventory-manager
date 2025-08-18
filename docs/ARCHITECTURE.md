# Project Architecture

## Overview
The **Inventory Manager** project follows a progressive design:
1. Week 2 – Procedural script.
2. Week 3 – Object-Oriented, modular package.
3. Week 4 – Test-driven development with high coverage.

---

## Folder Structure
```
inventory-manager/
├── docs
│   ├── ARCHITECTURE.md
│   ├── INDEX.md
│   ├── SETUP.md
│   └── TESTING.md
├── pytest.ini
├── README.md
├── setup.cfg
├── tests
│   ├── conftest.py
│   ├── requirements.txt
│   ├── test_core.py
│   ├── test_models_fixture.py
│   ├── test_models.py
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
│   ├── inventory_manager
│   │   ├── core.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── utils.py
│   ├── main.py
│   ├── pyproject.toml
│   ├── requirements.txt
└── week_5
    ├── api
    │   ├── app.py
    │   ├── __init__.py
    │   ├── __pycache__
    │   └── routes
    │       ├── __init__.py
    │       ├── products.py
    ├── Day_1
    │   └── hello.py
    ├── requirements.txt
    ├── tests
    │   ├── __pycache__
    │   └── test_api_integration.py
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
