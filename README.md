# 📦 Inventory Manager

A beginner-friendly Python project to practice Git workflows, environment setup, and core Python programming concepts, including data structures, procedural programming, error handling, and data validation using Pydantic.

---

## 🐍 Python Concepts Practiced

- Virtual environments (`venv`)
- The Zen of Python (`import this`)
- List comprehensions vs. for loops
- Equality (`==`) vs. identity (`is`)
- Git branching: `main` → `develop` → `feature/week_1`, `feature/week_2`
- Pull Request (PR) workflow for team collaboration

---

## 📅 Overview Week - 2

This week focused on mastering core Python data structures and procedural programming techniques, culminating in a real-world command-line tool to process inventory data from a CSV file.

---

## 📂 Project Structure
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

## 💻 How to Set Up & Run

### 🧪 1. Clone the Repository

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

# 📦 3. Install Dependencies
pip install pydantic


# 🚀 How to Run the Project
python process_inventory.py
```

## 🗓️ Daily Topics & Learnings

### ✅ Day 1: Lists & Tuples

- **Lists**: Creation, indexing, slicing, appending, and removing elements.
  - Common methods: `.append()`, `.extend()`, `.pop()`, `.sort()`
- **Tuples**: Syntax, immutability, and use-cases.
- **Key Distinction**:
  - Use **lists** for homogeneous, mutable collections.
  - Use **tuples** for heterogeneous, fixed data (e.g., return multiple values from a function).

---

### ✅ Day 2: Dictionaries & Sets

- **Dictionaries**: Key-value pairs, creation, accessing, updating.
  - Iteration with `.keys()`, `.values()`, `.items()`
- **Sets**: Unordered collections of unique items.
  - Use cases: duplicate removal, fast membership testing.
  - **Performance**:
    - Lookup in set: **O(1)**
    - Lookup in list: **O(n)**

---

### ✅ Day 3: Control Flow & Functions

- **Control Flow**: `if`, `elif`, `else`, `for`, `while`
- **Functions**:
  - Parameters and return values
  - Applied **Single Responsibility Principle (SRP)**:
    - Each function does one thing well
  - Used procedural decomposition for code clarity

---

### ✅ Day 4: File I/O & `csv` Module

- **File Handling**: Using `with open(...) as f:` for reading/writing plain text
- **CSV Handling**:
  - `csv.reader`: Basic row parsing
  - `csv.DictReader`: Structured row parsing using headers
- **CSV Pitfalls**: Manual parsing fails with commas in quoted fields

---

### ✅ Day 5: Error Handling & Data Validation with Pydantic

- **Error Handling**:
  - `try...except`
  - Specific exceptions: `FileNotFoundError`, `ValueError`, `ValidationError`
- **Pydantic**:
  - Defined `Product` model with type validations:
    - `quantity`: non-negative `int`
    - `price`: positive `float`
  - Caught validation issues and logged errors instead of crashing

---

## 🧪 Daily Drills

1. **Remove duplicates from a list** using `set()`
2. **Convert list of tuples into a dictionary**:
   ```python
   dict([("Alice", 80), ("Bob", 90)])


  # 🧱 Inventory Manager – Week 3

A continuation of the inventory processor project, this week applies **Object-Oriented Programming (OOP)** principles and project structuring best practices. The goal is to transform procedural code into a clean, modular, and extensible Python package.

---

## 📅 Overview – Week 3

This week focused on understanding and applying Object-Oriented Programming (OOP) concepts to refactor the inventory tool built in Week 2. By organizing code into classes and separating concerns, the project becomes easier to maintain, test, and extend.

---

## 🏗️ Project Structure for Week-3 (OOP Version)

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

## 💻 How to Set Up & Run

### 🔧 1. Clone the Repository
```bash
git clone <your-repo-url>
cd inventory-manager

# 🧪 2. Set Up Virtual Environment
virtualenv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

#📦 3. Install Dependencies
pip install -r requirements.txt

# 🚀 How to Run the Project
python main.py
```

📌 Key Concepts Practiced
```
🧱 Object-Oriented Programming (OOP)

✅ SRP & OCP principles (Clean Code)

🧪 Data validation with Pydantic

📁 Modular Python package design

🧼 Code quality tools: Black and Ruff
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