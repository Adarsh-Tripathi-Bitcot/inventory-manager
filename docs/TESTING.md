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


## Week 5 – Integration Testing

### Overview
- Used **Flask test client** with pytest for end-to-end request validation.
- No mocking of business logic — real `Inventory` class used.

### Test Coverage
- `GET /api/products` – Returns list of products.
- `GET /api/products/<id>` – Returns product details or `404`.
- `POST /api/products` – Creates product, returns `201`.
- `PUT /api/products/<id>` – Updates product.

### Tools
| Tool         | Purpose                  |
|--------------|--------------------------|
| Flask        | Web API framework        |
| pytest       | Testing framework        |
| pytest-cov   | Coverage reports         |
| pydantic     | Validation               |



## Week 6 – Flask + PostgreSQL API Testing

### Overview
- Focused on unit, integration, and end-to-end tests for a Flask + PostgreSQL API.
- Added database fixtures and mocking for external dependencies.
- Covered API, models, request/response schemas, and seeding scripts.

### Test Suite Structure
```
week_6/tests/
├── __init__.py
├── conftest.py
├── test_app.py
├── test_config.py
├── test_models.py
├── test_request_response_models.py
├── test_routes.py
└── test_seed.py
```

### Key Practices
- **Database Fixtures**
  - Temporary test database using `pytest` fixtures.
  - Rollback after each test to isolate tests.

- **Mocking External Calls**
  - Replaced network or file I/O operations to test API endpoints in isolation.

- **Integration Tests**
  - Verified CRUD endpoints:
    - `GET /api/products`
    - `GET /api/products/<id>`
    - `POST /api/products`
    - `PUT /api/products/<id>`
  - Confirmed proper response codes, JSON validation, and DB persistence.

- **Request/Response Model Testing**
  - Ensured `request_model.py` and `response_model.py` schemas validate payloads correctly.

- **Seed Script Testing**
  - Verified that `seed.py` populates the DB correctly.
  - Checked for duplicate handling and data consistency.

### Tools
| Tool           | Purpose                          |
|----------------|----------------------------------|
| Flask          | API framework                    |
| SQLAlchemy     | ORM for PostgreSQL               |
| Alembic        | DB migrations                    |
| psycopg2       | PostgreSQL driver                |
| pytest         | Test framework                   |
| pytest-mock    | Mocking support                  |
| pytest-cov     | Coverage reports                 |
| pydantic       | Request/response validation      |
| unittest.mock  | Mocking built-ins                |

### Achievements

- Full coverage of Flask + PostgreSQL API endpoints
- Isolated database tests using fixtures
- Mock-based tests for file or network dependencies
- Validated request/response schemas with Pydantic
- Ensured seed data scripts work as expected
- High test coverage and reliable TDD workflow for backend API



# Testing & TDD Practices – Week 7

## Overview
Week 7 emphasizes **security testing** and API validation:
- JWT login & authentication
- Role-based access control
- Integration with existing Flask + PostgreSQL endpoints
- Unit tests for security utilities
- Coverage >95% for security-related modules

---

## Test Suite Structure
```
tests/
├── test_security.py # Login, JWT, role checks
├── test_routes.py # Protected endpoints
├── test_models.py # User & Product models
├── conftest.py # Fixtures for client, test DB, users
```

---

## Key Practices

### 1. JWT Authentication
- Tested login with valid/invalid credentials
- Verified token issuance and expiration
- Ensured token is required for protected endpoints

### 2. Role-based Access
- `manager` can create/update products
- `staff` can only read products
- Tests assert **403 Forbidden** for unauthorized roles

### 3. Mocking External Dependencies
- Used `pytest-mock` to mock DB operations for security tests
- Ensured test isolation without touching production DB

### 4. Integration Tests
- Verified full request–response cycle with Flask test client
- Checked HTTP status codes, response payloads, and DB effects

---

## Tools
| Tool            | Purpose                        |
|-----------------|--------------------------------|
| Flask           | API framework                  |
| SQLAlchemy      | ORM for PostgreSQL             |
| Alembic         | Database migrations            |
| pytest          | Test framework                 |
| pytest-mock     | Mocking & patching             |
| pytest-cov      | Coverage reporting             |
| pydantic        | Validation of request payloads |
| bcrypt          | Password hashing               |

---

## Achievements
- JWT authentication implemented and tested
- Role-based restrictions validated
- CRUD endpoints secured
- High test coverage (>95%) for security and API routes
- End-to-end secure API workflow validated