"""Console UI client for POS operations."""

import sys

from tabulate import tabulate  # third-party
from src.db import SessionLocal, init_db  # first-party
from src.models import Product, Sale, SaleItem  # first-party


def add_product():
    """Prompt for product details and add to inventory."""
    with SessionLocal() as session:
        name = input("Product name: ").strip()
        price = float(input("Price: "))
        category = input("Category (optional): ").strip()
        prod = Product(name=name, price=price, category=category)
        session.add(prod)
        session.commit()
        print(f"Added product {prod.id} - {prod.name}")


def update_stock():
    """Prompt for product ID and new stock quantity."""
    with SessionLocal() as session:
        pid = int(input("Product ID: "))
        prod = session.get(Product, pid)
        if prod is None:
            print("Product not found.")
        else:
            qty = int(input("New stock quantity: "))
            prod.stock = qty  # type: ignore[attr-defined]
            session.commit()
            print(f"Stock updated: {prod.name} = {prod.stock}")


def search_products():
    """Search products by name or category."""
    with SessionLocal() as session:
        term = input("Search term: ").strip()
        results = session.query(Product).filter(
            (Product.name.ilike(f"%{term}%")) | (Product.category.ilike(f"%{term}%"))
        ).all()
        table = [(p.id, p.name, p.category, p.price, p.stock) for p in results]
        print(tabulate(table, headers=["ID", "Name", "Category", "Price", "Stock"]))


def record_sale():
    """Record a sale transaction."""
    with SessionLocal() as session:
        pid = int(input("Product ID: "))
        qty = int(input("Quantity: "))
        prod = session.get(Product, pid)
        if prod is None:
            print("Product not found.")
        elif prod.stock < qty:  # type: ignore[operator]
            print("Insufficient stock.")
        else:
            sale = Sale()
            _item = SaleItem(sale=sale, product=prod, quantity=qty, price=prod.price)
            prod.stock -= qty  # type: ignore[attr-defined]
            session.add(sale)
            session.commit()
            print(f"Sale recorded: {qty} x {prod.name} for ${qty * prod.price}")


def return_sale():
    """Cancel a sale and restock items."""
    with SessionLocal() as session:
        sid = int(input("Sale ID to return: "))
        sale = session.get(Sale, sid)
        if sale is None:
            print("Sale not found.")
        else:
            for item in sale.items:
                prod = session.get(Product, item.product_id)
                prod.stock += item.quantity  # type: ignore[attr-defined]
            session.delete(sale)
            session.commit()
            print(f"Sale {sid} returned.")


def show_stock_report():
    """Display current inventory stock report."""
    with SessionLocal() as session:
        products = session.query(Product).all()
        table = [(p.id, p.name, p.category, p.price, p.stock) for p in products]
        print(tabulate(table, headers=["ID", "Name", "Category", "Price", "Stock"]))


def main():
    """Main menu loop; database is auto-initialized."""
    # Ensure tables exist
    init_db()
    print("Database schema ensured.")
    # Define user actions
    actions = {
        '1': ('Add product', add_product),
        '2': ('Update stock', update_stock),
        '3': ('Search products', search_products),
        '4': ('Record sale', record_sale),
        '5': ('Return sale', return_sale),
        '6': ('Stock report', show_stock_report),
        '0': ('Exit', lambda: sys.exit(0)),
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
            print("Invalid selection, try again.")


if __name__ == '__main__':
    main()
