"""Console entry point orchestrating view/controller calls."""

import sys

from src.db import init_db
from src.views import cli_views


def main():
    """Main menu loop; database is auto-initialized."""
    # Ensure tables exist
    init_db()
    print("Database schema ensured.")
    actions = {
        '1': ('Add product', cli_views.add_product),
        '2': ('Update stock', cli_views.update_stock),
        '3': ('Search products', cli_views.search_products),
        '4': ('Record sale', cli_views.record_sale),
        '5': ('Return sale', cli_views.return_sale),
        '6': ('Stock report', cli_views.show_stock_report),
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
