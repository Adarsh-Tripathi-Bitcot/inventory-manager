# Setup & Installation

## Requirements
- Python 3.10+
- [Pydantic v2](https://docs.pydantic.dev)
- pytest, pytest-mock, pytest-cov (for tests)
- Black & Ruff (for formatting and linting)

---

## 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd inventory-manager

2️⃣ Create and Activate a Virtual Environment
Linux/macOS:
python -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate


3️⃣ Install Dependencies
pip install -r requirements.txt


4️⃣ Run the Application
Procedural (Week 2 version):
cd week_2
python process_inventory.py


OOP (Week 3 version):
python main.py


5️⃣ Run Tests
pytest
With coverage report:
pytest --cov=.



## 🖥️ Running the Flask API (Week 5)

1️⃣ Activate virtual environment:
```bash
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


2️⃣ Install dependencies:

pip install -r requirements.txt


3️⃣ Run the Flask API:

cd week_5/api
python -m week_5.api.app


API will be available at:

http://127.0.0.1:5000/api/products