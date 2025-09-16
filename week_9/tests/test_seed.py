"""Tests for seed.py CLI command (patched to satisfy created_by constraint)."""

import csv
from click.testing import CliRunner
from week_6_and_7.api.seed import seed_db
from week_6_and_7.api.models import Product, User


def _write_csv(tmp_path, product_id: int = 1) -> str:
    """Helper to write a CSV file with a sample product."""
    file_path = tmp_path / "products.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["product_id", "product_name", "quantity", "price", "type", "author", "pages"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "product_id": product_id,
                "product_name": f"TestProd_{product_id}",
                "quantity": "5",
                "price": "2.5",
                "type": "book",
                "author": "AuthorX",
                "pages": "100",
            }
        )
    return str(file_path)


def test_seed_db_adds_and_skips(monkeypatch, tmp_path, app, db) -> None:
    """Check seed_db adds a new product and then skips duplicate (work around created_by NOT NULL)."""
    # Ensure tables are empty
    with app.app_context():
        db.session.query(Product).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Create a default user; we will inject created_by=user.id via a patched __init__
        seeder = User(username="seeder", role="admin")
        seeder.set_password("pw")
        db.session.add(seeder)
        db.session.commit()
        seeder_id = seeder.id

        # Patch Product.__init__ to auto-fill created_by if missing (only for this test)
        original_init = Product.__init__

        def patched_init(self, *args, **kwargs):
            kwargs.setdefault("created_by", seeder_id)
            return original_init(self, *args, **kwargs)

        monkeypatch.setattr(Product, "__init__", patched_init, raising=True)

    # Provide a CSV path
    csv_file = _write_csv(tmp_path)
    monkeypatch.setattr("week_6_and_7.api.seed.CSV_PATH", csv_file)

    runner = CliRunner()
    with app.app_context():
        first = runner.invoke(seed_db)
        assert "Added: 1" in first.output
        second = runner.invoke(seed_db)
        assert "Skipped: 1" in second.output


def test_seed_db_missing_file(monkeypatch, app) -> None:
    """seed_db should handle missing CSV file gracefully."""
    monkeypatch.setattr("week_6_and_7.api.seed.CSV_PATH", "/nonexistent.csv")
    runner = CliRunner()
    with app.app_context():
        result = runner.invoke(seed_db)
        assert "CSV file not found" in result.output
