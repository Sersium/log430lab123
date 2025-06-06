"""Console view functions for user interaction."""

from tabulate import tabulate

from src.controllers import (
    add_product as ctrl_add_product,
    update_stock as ctrl_update_stock,
    search_products as ctrl_search_products,
    record_sale as ctrl_record_sale,
    return_sale as ctrl_return_sale,
    get_stock_report as ctrl_get_stock_report,
    generate_sales_report as ctrl_generate_sales_report,
    request_replenishment as ctrl_request_replenishment,
    get_dashboard_metrics as ctrl_get_dashboard_metrics,
    generate_hq_sales_report as ctrl_generate_hq_sales_report,
    get_hq_stock as ctrl_get_hq_stock,
)


def add_product():
    """Prompt for product details and display result."""
    name = input("Product name: ").strip()
    while True:
        try:
            price = float(input("Price: "))
            break
        except ValueError:
            print("Invalid price. Please enter a numeric value.")
    category = input("Category (optional): ").strip()
    store_id = int(input("Store ID: "))
    prod = ctrl_add_product(name, price, category, store_id)
    print(f"Added product {prod.id} - {prod.name}")


def update_stock():
    """Prompt for product ID and new stock quantity."""
    pid = int(input("Product ID: "))
    qty = int(input("New stock quantity: "))
    prod = ctrl_update_stock(pid, qty)
    if prod is None:
        print("Product not found.")
    else:
        print(f"Stock updated: {prod.name} = {prod.stock}")


def search_products():
    """Prompt for a search term and display matching products."""
    term = input("Search term: ").strip()
    store_id = int(input("Store ID (blank for all): ") or 0)
    results = ctrl_search_products(term, store_id if store_id else None)
    table = [(p.id, p.name, p.category, p.price, p.stock) for p in results]
    print(tabulate(table, headers=["ID", "Name", "Category", "Price", "Stock"]))


def record_sale():
    """Record a sale transaction via prompts."""
    pid = int(input("Product ID: "))
    qty = int(input("Quantity: "))
    sale = ctrl_record_sale(pid, qty)
    if sale is None:
        print("Product not found or insufficient stock.")
    else:
        item = sale.items[0]
        print(
            f"Sale recorded: {item.quantity} x {item.product.name} for ${item.quantity * item.price}"
        )


def return_sale():
    """Prompt for sale ID to cancel."""
    sid = int(input("Sale ID to return: "))
    if ctrl_return_sale(sid):
        print(f"Sale {sid} returned.")
    else:
        print("Sale not found.")


def show_stock_report():
    """Display inventory information."""
    store_id = int(input("Store ID (blank for all): ") or 0)
    products = ctrl_get_stock_report(store_id if store_id else None)
    table = [(p.id, p.name, p.category, p.price, p.stock) for p in products]
    print(tabulate(table, headers=["ID", "Name", "Category", "Price", "Stock"]))


def sales_report():
    """Display consolidated sales information for all stores."""
    report = ctrl_generate_sales_report()
    print("\nRevenue by store:")
    print(tabulate(report["stores"], headers=["Store", "Revenue"]))
    print("\nTop products:")
    print(tabulate(report["top_products"], headers=["Product", "Qty"]))
    print("\nCurrent stock:")
    print(tabulate(report["stock"], headers=["Product", "Stock", "Store"]))


def handle_replenishment():
    """Request stock from the central warehouse."""
    store_id = int(input("Store ID: "))
    product_id = int(input("Product ID: "))
    qty = int(input("Quantity to request: "))
    if ctrl_request_replenishment(store_id, product_id, qty):
        print("Replenishment successful.")
    else:
        print("Insufficient stock in central warehouse or invalid IDs.")


def show_dashboard():
    """Display high level KPIs for management."""
    metrics = ctrl_get_dashboard_metrics()
    print("\nRevenue by store:")
    print(tabulate(metrics["revenue"], headers=["Store", "Revenue"]))
    print("\nOut of stock:")
    print(tabulate(metrics["out_of_stock"], headers=["Product", "Store"]))
    print("\nOverstock (>100):")
    print(tabulate(metrics["overstock"], headers=["Product", "Store", "Qty"]))
    print("\nWeekly trends:")
    print(tabulate(metrics["weekly"], headers=["Week", "Store", "Revenue"]))



def hq_stock_report():
    """Display current HQ warehouse stock."""
    stock = ctrl_get_hq_stock()
    print(tabulate(stock, headers=["Product", "Qty"]))


def hq_sales_report():
    """Display sales report using HQ data."""
    report = ctrl_generate_hq_sales_report()
    print("\nRevenue by store:")
    print(tabulate(report["stores"], headers=["Store", "Revenue"]))
    print("\nTop products:")
    print(tabulate(report["top_products"], headers=["Product", "Qty"]))
    print("\nCurrent stock:")
    print(tabulate(report["stock"], headers=["Product", "Stock", "Store"]))
