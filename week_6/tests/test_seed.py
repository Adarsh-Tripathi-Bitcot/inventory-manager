"""Tests for seed.py CLI command."""

import csv
from click.testing import CliRunner
from week_6.api.seed import seed_db
from week_6.api.models import Product


def _write_csv(tmp_path, product_id: int = 1) -> str:
    """Helper to write a CSV file with a sample product."""
    file_path = tmp_path / "products.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["product_id", "product_name", "quantity", "price", "type", "author", "pages"]
        )
        writer.writeheader()
        writer.writerow({
            "product_id": product_id,
            "product_name": f"TestProd_{product_id}",
            "quantity": "5",
            "price": "2.5",
            "type": "book",
            "author": "AuthorX",
            "pages": "100"
        })
    return str(file_path)


def test_seed_db_adds_and_skips(monkeypatch, tmp_path, app, db) -> None:
    """Check seed_db adds a new product and skips duplicates."""
    with app.app_context():
        db.session.query(Product).delete()
        db.session.commit()

    csv_file = _write_csv(tmp_path)
    monkeypatch.setattr("week_6.api.seed.CSV_PATH", csv_file)

    runner = CliRunner()
    with app.app_context():
        first = runner.invoke(seed_db)
        assert "Added: 1" in first.output
        second = runner.invoke(seed_db)
        assert "Skipped: 1" in second.output


def test_seed_db_missing_file(monkeypatch, app) -> None:
    """seed_db should handle missing CSV file gracefully."""
    monkeypatch.setattr("week_6.api.seed.CSV_PATH", "/nonexistent.csv")
    runner = CliRunner()
    with app.app_context():
        result = runner.invoke(seed_db)
        assert "CSV file not found" in result.output
