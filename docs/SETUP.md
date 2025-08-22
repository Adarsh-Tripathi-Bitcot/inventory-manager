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