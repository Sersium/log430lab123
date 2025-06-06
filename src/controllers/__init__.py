"""Business logic layer for POS operations."""

from typing import Dict, List, Optional

from sqlalchemy import func

from src.db import HQSession, SessionLocal
from src.models import CentralStock, Product, Sale, SaleItem, Store


def add_product(name: str, price: float, category: str, store_id: int) -> Product:
    """Create a new product for a given store and sync to HQ."""
    # ensure we have latest data from HQ
    sync_from_hq()
    session = SessionLocal()
    try:
        prod = Product(name=name, price=price, category=category, store_id=store_id)
        session.add(prod)
        session.commit()
        session.refresh(prod)
    finally:
        session.close()
    # push changes to HQ database
    sync_to_hq()
    return prod


def update_stock(product_id: int, quantity: int) -> Optional[Product]:
    """Update stock quantity for a product and sync."""
    sync_from_hq()
    session = SessionLocal()
    try:
        prod = session.get(Product, product_id)
        if prod is None:
            return None
        prod.stock = quantity  # type: ignore[attr-defined]
        session.commit()
        session.refresh(prod)
    finally:
        session.close()
    sync_to_hq()
    return prod


def search_products(term: str, store_id: int | None = None) -> List[Product]:
    """Return products matching the search term for a store."""
    session = SessionLocal()
    try:
        query = session.query(Product).filter(
            (Product.name.ilike(f"%{term}%")) | (Product.category.ilike(f"%{term}%"))
        )
        if store_id is not None:
            query = query.filter(Product.store_id == store_id)
        return query.all()
    finally:
        session.close()


def record_sale(product_id: int, quantity: int) -> Optional[Sale]:
    """Record a sale transaction if stock allows and sync."""
    sync_from_hq()
    session = SessionLocal()
    try:
        prod = session.get(Product, product_id)
        if prod is None or prod.stock < quantity:  # type: ignore[operator]
            return None
        sale = Sale(store_id=prod.store_id)
        _item = SaleItem(
            sale=sale,
            product=prod,
            quantity=quantity,
            price=prod.price,
        )
        prod.stock -= quantity  # type: ignore[attr-defined]
        session.add(sale)
        session.commit()
        session.refresh(sale)
    finally:
        session.close()
    sync_to_hq()
    return sale


def return_sale(sale_id: int) -> bool:
    """Cancel a sale, restock items and sync."""
    sync_from_hq()
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
    finally:
        session.close()
    sync_to_hq()
    return True


def get_stock_report(store_id: int | None = None) -> List[Product]:
    """Return a list of products for reporting for a given store."""
    session = SessionLocal()
    try:
        query = session.query(Product)
        if store_id is not None:
            query = query.filter(Product.store_id == store_id)
        return query.all()
    finally:
        session.close()


def generate_sales_report() -> Dict[str, List]:
    """Return consolidated sales report data for all stores."""
    session = SessionLocal()
    try:
        return _generate_report_for_session(session)
    finally:
        session.close()


def request_replenishment(store_id: int, product_id: int, quantity: int) -> bool:
    """Transfer stock from the central warehouse to a store if available."""
    sync_from_hq()
    session = SessionLocal()
    try:
        central = (
            session.query(CentralStock)
            .filter(CentralStock.product_id == product_id)
            .first()
        )
        product = session.query(Product).filter(
            Product.id == product_id, Product.store_id == store_id
        ).first()
        if central is None or product is None or central.quantity < quantity:
            return False

        central.quantity -= quantity
        product.stock += quantity  # type: ignore[attr-defined]
        session.commit()
    finally:
        session.close()
    sync_to_hq()
    return True


def get_dashboard_metrics() -> Dict[str, List]:
    """Return high level performance indicators for all stores."""
    session = SessionLocal()
    try:
        # Revenue per store
        revenue = (
            session.query(
                Store.name,
                func.sum(SaleItem.quantity * SaleItem.price).label("revenue"),
            )
            .join(Sale)
            .join(SaleItem)
            .group_by(Store.name)
            .all()
        )

        # Products with zero stock trigger an alert
        out_of_stock = (
            session.query(Product.name, Store.name)
            .join(Store)
            .filter(Product.stock <= 0)
            .all()
        )

        # Very high stock could indicate overstock
        overstock = (
            session.query(Product.name, Store.name, Product.stock)
            .join(Store)
            .filter(Product.stock > 100)
            .all()
        )

        # Weekly revenue trends per store
        weekly = (
            session.query(
                func.date_trunc("week", Sale.timestamp).label("week"),
                Store.name,
                func.sum(SaleItem.quantity * SaleItem.price).label("revenue"),
            )
            .join(Store)
            .join(SaleItem)
            .group_by("week", Store.name)
            .order_by("week")
            .all()
        )

        return {
            "revenue": revenue,
            "out_of_stock": out_of_stock,
            "overstock": overstock,
            "weekly": weekly,
        }
    finally:
        session.close()


def sync_to_hq() -> bool:
    """Push local data to the HQ database."""
    if HQSession is SessionLocal:
        return False
    local = SessionLocal()
    hq = HQSession()
    try:
        for model in (Store, Product, Sale, SaleItem, CentralStock):
            for obj in local.query(model).all():
                hq.merge(obj)
        hq.commit()
        return True
    finally:
        local.close()
        hq.close()


def sync_from_hq() -> bool:
    """Pull data from the HQ database into the local store."""
    if HQSession is SessionLocal:
        return False
    local = SessionLocal()
    hq = HQSession()
    try:
        for model in (Store, Product, CentralStock):
            for obj in hq.query(model).all():
                local.merge(obj)
        for sale in hq.query(Sale).all():
            local.merge(sale)
            for item in sale.items:
                local.merge(item)
        local.commit()
        return True
    finally:
        local.close()
        hq.close()


def generate_hq_sales_report() -> Dict[str, List]:
    """Generate a sales report using the HQ database."""
    if HQSession is SessionLocal:
        return generate_sales_report()
    session = HQSession()
    try:
        return _generate_report_for_session(session)
    finally:
        session.close()


def _generate_report_for_session(session) -> Dict[str, List]:
    """Helper to generate sales report using a provided session."""
    store_data = []
    for store in session.query(Store).all():
        revenue = (
            session.query(func.sum(SaleItem.quantity * SaleItem.price))
            .join(Sale)
            .filter(Sale.store_id == store.id)
            .scalar()
            or 0.0
        )
        store_data.append({"store": store.name, "revenue": float(revenue)})

    top_products = (
        session.query(
            Product.name,
            func.sum(SaleItem.quantity).label("qty"),
        )
        .join(SaleItem, SaleItem.product_id == Product.id)
        .group_by(Product.name)
        .order_by(func.sum(SaleItem.quantity).desc())
        .limit(5)
        .all()
    )

    stock = (
        session.query(Product.name, Product.stock, Store.name)
        .join(Store, Product.store_id == Store.id)
        .all()
    )

    return {"stores": store_data, "top_products": top_products, "stock": stock}


def get_hq_stock() -> List[tuple[str, int]]:
    """Return the current HQ warehouse stock."""
    session = HQSession()
    try:
        return (
            session.query(Product.name, CentralStock.quantity)
            .join(CentralStock, CentralStock.product_id == Product.id)
            .order_by(Product.name)
            .all()
        )
    finally:
        session.close()
