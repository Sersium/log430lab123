"""CLI views for headquarters operations."""

import os
from tabulate import tabulate
from src.models import Product
from . import controllers

controllers.set_logistics_url(os.getenv("LOGISTICS_URL", "sqlite:///logistics.db"))


def sync_product_to_store(store, product):
    controllers.sync_product_to_store(store, product)


def add_or_update_product() -> None:
    pid = input("Product ID (blank to create new): ").strip()
    if pid:
        prod = Product(id=int(pid))
    else:
        prod = Product()
    prod.name = input("Name: ")
    prod.price = float(input("Price: "))
    prod.category = input("Category: ") or None
    updated = controllers.add_or_update_product(prod)
    print(f"Product {updated.id} synced to stores")


def consolidated_report() -> None:
    totals = controllers.consolidated_report()
    print(tabulate(totals, headers=["Store", "Total Sales"]))


def main() -> None:
    actions = {
        "1": ("Add/update product", add_or_update_product),
        "2": ("Consolidated sales report", consolidated_report),
        "0": ("Exit", lambda: exit(0)),
    }
    while True:
        for key, (desc, _) in actions.items():
            print(f"{key}. {desc}")
        choice = input("Select: ")
        action = actions.get(choice)
        if action:
            action[1]()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
