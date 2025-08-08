# 🏗️ Project Architecture

## Overview
The **Inventory Manager** project follows a progressive design:
1. Week 2 – Procedural script.
2. Week 3 – Object-Oriented, modular package.
3. Week 4 – Test-driven development with high coverage.

---

## Folder Structure
```
inventory-manager/
├── week_1/ # Python basics practice
├── week_2/ # Procedural version
│ ├── process_inventory.py
│ ├── csv_utils.py
│ ├── pydantic_utils.py
│ └── ...
├── week_3/ # OOP version (main package)
│ └── inventory_manager/
│ ├── init.py
│ ├── core.py # Inventory business logic
│ ├── models.py # Product models (Pydantic)
│ ├── utils.py # Logging helpers
│ └── data/ # Sample CSVs
├── tests/ # Pytest test suite
│ ├── conftest.py
│ ├── test_core.py
│ ├── test_models.py
│ └── ...
├── requirements.txt
├── pytest.ini
└── README.md
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
