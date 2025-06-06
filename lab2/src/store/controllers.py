from __future__ import annotations

"""Business logic for store operations (MVC controller layer)."""

import os
from typing import List, Optional

from src.db import SessionLocal, init_db, session_for_url
from src.models import Product, Sale, SaleItem
from logistics.models import RestockRequest


# Ensure DB is initialized when module functions are used
init_db()


def create_product(name: str, price: float, category: Optional[str] = None) -> Product:
    """Create a product and persist it."""
    with SessionLocal() as session:
        prod = Product(name=name, price=price, category=category)
        session.add(prod)
        session.commit()
        session.refresh(prod)
        return prod


def set_stock(product_id: int, quantity: int) -> Optional[Product]:
    """Update stock quantity for a product."""
    with SessionLocal() as session:
        prod = session.get(Product, product_id)
        if not prod:
            return None
        prod.stock = quantity  # type: ignore[attr-defined]
        session.commit()
        return prod


def find_products(term: str) -> List[Product]:
    """Search products by name or category."""
    with SessionLocal() as session:
        return session.query(Product).filter(
            (Product.name.ilike(f"%{term}%")) | (Product.category.ilike(f"%{term}%"))
        ).all()


def create_sale(product_id: int, quantity: int) -> Optional[Sale]:
    """Record a sale and decrement product stock."""
    with SessionLocal() as session:
        prod = session.get(Product, product_id)
        if not prod or prod.stock < quantity:  # type: ignore[operator]
            return None
        sale = Sale()
        SaleItem(sale=sale, product=prod, quantity=quantity, price=prod.price)
        prod.stock -= quantity  # type: ignore[attr-defined]
        session.add(sale)
        session.commit()
        session.refresh(sale)
        return sale


def cancel_sale(sale_id: int) -> bool:
    """Return a sale and restock items."""
    with SessionLocal() as session:
        sale = session.get(Sale, sale_id)
        if not sale:
            return False
        for item in sale.items:
            prod = session.get(Product, item.product_id)
            prod.stock += item.quantity  # type: ignore[attr-defined]
        session.delete(sale)
        session.commit()
        return True


def list_inventory() -> List[Product]:
    """Return all products with stock info."""
    with SessionLocal() as session:
        return session.query(Product).all()


def request_restock(product_id: int, quantity: int) -> Optional[RestockRequest]:
    """Send a restock request to the logistics database."""
    logistics_url = os.getenv("LOGISTICS_URL")
    if not logistics_url:
        return None
    store_id = int(os.getenv("STORE_ID", "1"))
    LogisticsSession = session_for_url(logistics_url)
    with LogisticsSession() as session:
        req = RestockRequest(store_id=store_id, product_id=product_id, quantity=quantity)
        session.add(req)
        session.commit()
        session.refresh(req)
        return req

