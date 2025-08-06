import pytest
import tempfile
import os
from inventory_manager.core import Inventory
from inventory_manager.models import Product


@pytest.fixture
def sample_products():
    return [
        Product(product_id="1", product_name="Pen", quantity=5, price=10.0),
        Product(product_id="2", product_name="Notebook", quantity=20, price=50.0),
        Product(product_id="3", product_name="Marker", quantity=3, price=15.0),
    ]


@pytest.fixture
def inventory_with_products(sample_products):
    inv = Inventory()
    inv.products.extend(sample_products)
    return inv


def test_inventory_initialization():
    inv = Inventory()
    assert isinstance(inv.products, list)
    assert len(inv.products) == 0


def test_generate_low_stock_report(tmp_path, inventory_with_products):
    # Set the current directory to the temporary path to avoid polluting real files
    cwd = os.getcwd()
    os.chdir(tmp_path)

    inventory_with_products.generate_low_stock_report(threshold=10)

    # Assert the file is created
    report_file = tmp_path / "low_stock_report.txt"
    assert report_file.exists()

    # Check file content
    content = report_file.read_text()
    assert "Pen" in content
    assert "Marker" in content
    assert "Notebook" not in content

    os.chdir(cwd)


def test_generate_low_stock_report_handles_exception(monkeypatch, inventory_with_products):
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("Test error")))
    inventory_with_products.generate_low_stock_report()


def test_print_summary_dashboard(capsys, inventory_with_products):
    inventory_with_products.print_summary_dashboard()
    output = capsys.readouterr().out

    assert "INVENTORY SUMMARY DASHBOARD" in output
    assert "TOTAL PRODUCTS" in output
    assert "TOTAL QUANTITY" in output
    assert "HIGHEST SALE PRODUCT" in output
    assert "Total inventory value" in output


def test_print_summary_dashboard_handles_exception(monkeypatch, inventory_with_products):
    calls = {"count": 0}

    def mock_print(*args, **kwargs):
        if calls["count"] == 0:
            calls["count"] += 1
            raise Exception("Test Print Error")
        else:
            original_print(*args, **kwargs)

    original_print = print
    monkeypatch.setattr("builtins.print", mock_print)

    # Should not raise
    inventory_with_products.print_summary_dashboard()


def test_load_from_csv_valid(tmp_path):
    # Create a valid CSV file
    csv_content = """product_id,product_name,quantity,price,type,expiry_date,warranty_period,author,pages
1,Banana,20,5.0,food,2025-12-31,,,
2,Laptop,5,50000.0,electronic,,12,,
3,Book ABC,10,200.0,book,,,Author Name,150
4,GenericItem,10,10.0,,,,,
"""
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(csv_content)

    inventory = Inventory()
    inventory.load_from_csv(str(csv_file))

    assert len(inventory.products) == 4
    names = [p.product_name for p in inventory.products]
    assert "Banana" in names
    assert "Laptop" in names
    assert "Book ABC" in names
    assert "GenericItem" in names


def test_load_from_csv_invalid(tmp_path):
    # One row has negative quantity, another missing price
    csv_content = """product_id,product_name,quantity,price,type
1,InvalidItem1,-5,10.0,food
2,InvalidItem2,5,,electronic
"""
    csv_file = tmp_path / "invalid_products.csv"
    csv_file.write_text(csv_content)

    # Clear previous error log if exists
    if os.path.exists("errors.log"):
        os.remove("errors.log")

    inventory = Inventory()
    inventory.load_from_csv(str(csv_file))

    assert len(inventory.products) == 0

    # Check that errors were logged
    with open("errors.log", "r") as f:
        content = f.read()
        assert "Row 2:" in content
        assert "Row 3:" in content


def test_load_from_csv_file_not_found():
    inventory = Inventory()
    inventory.load_from_csv("non_existent.csv")  # Should not crash
