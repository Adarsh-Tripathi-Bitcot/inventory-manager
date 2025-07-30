# Inventory Manager

A beginner-friendly Python project to practice Git workflows, environment setup, and basic Python syntax.


## 🐍 Python Concepts Practiced

- Virtual environments (`venv`)
- The Zen of Python (`import this`)
- List comprehensions vs. for loops
- Equality (`==`) vs. identity (`is`)
- Git branching: `main` → `develop` → `feature/initial-setup`
- Pull Request (PR) workflow for team collaboration

# 🧠 Week 2: Python Data Structures & Procedural Programming

## 📅 Overview

This week focused on mastering core Python data structures and procedural programming techniques, culminating in a real-world command-line tool to process inventory data from a CSV file.

---

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

