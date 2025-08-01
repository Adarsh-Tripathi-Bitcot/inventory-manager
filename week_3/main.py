# main.py
from inventory_manager.core import Inventory

if __name__ == "__main__":
    inventory = Inventory()
    inventory.load_from_csv("data/products.csv")
    inventory.generate_low_stock_report(threshold=10)
