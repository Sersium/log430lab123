"""CLI views for logistics service."""

from . import controllers


def list_stock() -> None:
    for row in controllers.list_stock():
        print(f"{row.product.name}: {row.quantity}")


def register_store(name: str | None = None, db_url: str | None = None) -> None:
    if name is None:
        name = input("Store name: ")
    if db_url is None:
        db_url = input("Store DB URL: ")
    store = controllers.register_store(name, db_url)
    print(f"Registered store {store.id} -> {store.db_url}")


def approve_request_by_id(rid: int):
    """Expose controller function for tests."""
    return controllers.approve_request_by_id(rid)


def approve_request() -> None:
    rid = int(input("Request ID: "))
    req = controllers.approve_request_by_id(rid)
    if req:
        print("Request approved")
    else:
        print("Could not approve request")


if __name__ == "__main__":
    controllers.init_logistics_db()
    actions = {
        "1": ("List stock", list_stock),
        "2": ("Approve restock request", approve_request),
        "3": ("Register store", register_store),
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
            print("Invalid")

