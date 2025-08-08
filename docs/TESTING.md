# Testing & TDD Practices

## Overview
Week 4 focused on building a strong **Test-Driven Development (TDD)** habit with pytest:
- **Red–Green–Refactor** cycle
- Reusable **fixtures** for setup
- **Mocking & patching** for file I/O
- **Parametrized tests** for multiple scenarios
- Coverage analysis

---

## Test Suite Structure
```
tests/
├── conftest.py
├── test_core.py
├── test_models.py
├── test_models_fixture.py
├── test_inventory.py
```


## Key Practices
### 1. TDD Cycle
1. Write failing test (Red)  
2. Write minimal code to pass (Green)  
3. Refactor with tests passing (Refactor)

### 2. Fixtures
- Example: `base_product`, `inventory` used across multiple tests.

### 3. Mocking & Patching
- Used `pytest-mock` to replace:
  - `open()` calls in `load_from_csv`
  - File writes in `generate_low_stock_report`

### 4. Parametrization
- Tested multiple invalid data cases without duplicate code.

### 5. Coverage
- Used `pytest-cov` to measure coverage.
- Achieved **>95%** coverage for the package.

---

## Tools Used
| Tool         | Purpose |
|--------------|---------|
| pytest       | Test framework |
| pytest-mock  | Mocking support |
| pytest-cov   | Coverage reports |
| pydantic     | Model validation |
| unittest.mock| Mocking built-ins |

---

## Achievements
- Comprehensive test suite for `inventory_manager`
- Mock-based tests for file I/O without touching the filesystem
- Parametrization reduced test duplication
- High coverage with meaningful assertions
