"""Business logic layer for POS operations."""

from typing import List, Optional

from src.db import SessionLocal
from src.models import Product, Sale, SaleItem


def add_product(name: str, price: float, category: str) -> Product:
    """Create a new product and persist it."""
    session = SessionLocal()
    try:
        prod = Product(name=name, price=price, category=category)
        session.add(prod)
        session.commit()
        session.refresh(prod)
        return prod
    finally:
        session.close()


def update_stock(product_id: int, quantity: int) -> Optional[Product]:
    """Update stock quantity for a product."""
    session = SessionLocal()
    try:
        prod = session.get(Product, product_id)
        if prod is None:
            return None
        prod.stock = quantity  # type: ignore[attr-defined]
        session.commit()
        session.refresh(prod)
        return prod
    finally:
        session.close()


def search_products(term: str) -> List[Product]:
    """Return products matching the search term."""
    session = SessionLocal()
    try:
        results = (
            session.query(Product)
            .filter(
                (Product.name.ilike(f"%{term}%"))
                | (Product.category.ilike(f"%{term}%"))
            )
            .all()
        )
        return results
    finally:
        session.close()


def record_sale(product_id: int, quantity: int) -> Optional[Sale]:
    """Record a sale transaction if stock allows."""
    session = SessionLocal()
    try:
        prod = session.get(Product, product_id)
        if prod is None or prod.stock < quantity:  # type: ignore[operator]
            return None
        sale = Sale()
        _item = SaleItem(sale=sale, product=prod, quantity=quantity, price=prod.price)
        prod.stock -= quantity  # type: ignore[attr-defined]
        session.add(sale)
        session.commit()
        session.refresh(sale)
        return sale
    finally:
        session.close()


def return_sale(sale_id: int) -> bool:
    """Cancel a sale and restock items."""
    session = SessionLocal()
    try:
        sale = session.get(Sale, sale_id)
        if sale is None:
            return False
        for item in sale.items:
            prod = session.get(Product, item.product_id)
            if prod:
                prod.stock += item.quantity  # type: ignore[attr-defined]
        session.delete(sale)
        session.commit()
        return True
    finally:
        session.close()


def get_stock_report() -> List[Product]:
    """Return a list of all products for reporting."""
    session = SessionLocal()
    try:
        return session.query(Product).all()
    finally:
        session.close()
