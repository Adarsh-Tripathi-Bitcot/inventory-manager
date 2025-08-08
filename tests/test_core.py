import pytest
from unittest.mock import patch, mock_open
from inventory_manager.core import Inventory
from inventory_manager.models import FoodProduct, ElectronicProduct
from pathlib import Path

MOCK_CSV_DATA = """product_id,product_name,quantity,price,category,expiry_date,warranty_period,author
F1,Apple,10,1.2,food,2025-12-01,, 
E1,Laptop,2,500.0,electronic,,2,
B1,Book,-1,0.0,book,,,John Doe
"""

def test_load_from_csv_with_mocked_data() -> None:
    """Test loading valid and invalid rows from mocked CSV."""
    inventory = Inventory()
    with patch("builtins.open", mock_open(read_data=MOCK_CSV_DATA)):
        inventory.load_from_csv("dummy_path.csv")
    
    assert len(inventory.products) == 2
    assert isinstance(inventory.products[0], FoodProduct)
    assert isinstance(inventory.products[1], ElectronicProduct)


def test_generate_low_stock_report(tmp_path: Path) -> None:
    """Test low stock report includes only products below threshold."""
    report_path = tmp_path / "report.txt"
    inventory = Inventory()
    inventory.products = [
        FoodProduct(product_id="F1", product_name="Apple", quantity=3, price=2.0, expiry_date="2025-12-01"),
        ElectronicProduct(product_id="E1", product_name="Laptop", quantity=10, price=500.0, warranty_period=2),
    ]
    inventory.generate_low_stock_report(report_path)
    report_text = report_path.read_text()
    assert "Apple" in report_text
    assert "Laptop" not in report_text


def test_generate_low_stock_report_no_low_stock(tmp_path: Path) -> None:
    """Test report message when all products are sufficiently stocked."""
    report_path = tmp_path / "report.txt"
    inventory = Inventory()
    inventory.products = [
        FoodProduct(product_id="F1", product_name="Apple", quantity=10, price=1.2, expiry_date="2025-12-01")
    ]
    inventory.generate_low_stock_report(report_path)
    content = report_path.read_text()
    assert "sufficiently stocked" in content


def test_print_summary_dashboard(capsys: pytest.CaptureFixture) -> None:
    """Test that the dashboard summary includes total and top product info."""
    inventory = Inventory()
    inventory.products = [
        FoodProduct(product_id="F1", product_name="Apple", quantity=10, price=2.0, expiry_date="2025-12-01"),
        ElectronicProduct(product_id="E1", product_name="Laptop", quantity=2, price=500.0, warranty_period=2),
    ]
    inventory.print_summary_dashboard()
    captured = capsys.readouterr()
    normalized = " ".join(captured.out.split())
    assert "Total Products" in normalized
    assert "Highest Sale Product" in normalized


def test_print_summary_dashboard_no_sales(capsys: pytest.CaptureFixture) -> None:
    """Test dashboard message when total sales are zero."""
    inventory = Inventory()
    inventory.products = [
        FoodProduct(product_id="F1", product_name="Apple", quantity=0, price=1.0, expiry_date="2025-12-01")
    ]
    inventory.print_summary_dashboard()
    captured = capsys.readouterr()
    assert "Highest Sale Product" in captured.out
