"""CLI views for store operations (MVC view layer)."""

from tabulate import tabulate

from . import controllers


def add_product() -> None:
    name = input("Product name: ")
    price = float(input("Price: "))
    category = input("Category (optional): ").strip() or None
    prod = controllers.create_product(name, price, category)
    print(f"Added product {prod.id} - {prod.name}")


def update_stock() -> None:
    pid = int(input("Product ID: "))
    qty = int(input("New stock quantity: "))
    prod = controllers.set_stock(pid, qty)
    if prod:
        print(f"Stock updated: {prod.name} = {prod.stock}")
    else:
        print("Product not found")


def search_products() -> None:
    term = input("Search term: ")
    results = controllers.find_products(term)
    table = [(p.id, p.name, p.category, p.price, p.stock) for p in results]
    print(tabulate(table, headers=["ID", "Name", "Category", "Price", "Stock"]))


def record_sale() -> None:
    pid = int(input("Product ID: "))
    qty = int(input("Quantity: "))
    sale = controllers.create_sale(pid, qty)
    if sale:
        print(f"Sale {sale.id} recorded")
    else:
        print("Sale could not be recorded")


def return_sale() -> None:
    sid = int(input("Sale ID to return: "))
    if controllers.cancel_sale(sid):
        print(f"Sale {sid} returned")
    else:
        print("Sale not found")


def show_stock_report() -> None:
    products = controllers.list_inventory()
    table = [(p.id, p.name, p.category, p.price, p.stock) for p in products]
    print(tabulate(table, headers=["ID", "Name", "Category", "Price", "Stock"]))


def request_restock() -> None:
    pid = int(input("Product ID to restock: "))
    qty = int(input("Quantity needed: "))
    req = controllers.request_restock(pid, qty)
    if req:
        print(f"Restock request {req.id} created")
    else:
        print("LOGISTICS_URL environment variable required")


def main() -> None:
    actions = {
        "1": ("Add product", add_product),
        "2": ("Update stock", update_stock),
        "3": ("Search products", search_products),
        "4": ("Record sale", record_sale),
        "5": ("Return sale", return_sale),
        "6": ("Stock report", show_stock_report),
        "7": ("Request restock", request_restock),
        "0": ("Exit", lambda: exit(0)),
    }
    while True:
        print("\nPoint of Sale - Main Menu")
        for key, (desc, _) in actions.items():
            print(f" {key}. {desc}")
        choice = input("Select an option: ").strip()
        action = actions.get(choice)
        if action:
            action[1]()
        else:
            print("Invalid selection")


if __name__ == "__main__":
    main()
