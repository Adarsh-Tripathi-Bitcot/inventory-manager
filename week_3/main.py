from inventory_manager.core import Inventory

def main():
    inventory = Inventory()
    inventory.load_from_csv("data/products.csv")
    inventory.generate_low_stock_report(threshold=10)
    inventory.print_summary_dashboard()  
    
if __name__ == "__main__":
    main()
