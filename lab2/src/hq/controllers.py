"""Business logic for headquarters operations."""

from typing import List

from src.db import session_for_url, init_db
from src.models import Product, SaleItem
from logistics.models import Store

LOGISTICS_URL = "sqlite:///logistics.db"


def set_logistics_url(url: str) -> None:
    global LOGISTICS_URL
    LOGISTICS_URL = url


def _logistics_session():
    init_db(LOGISTICS_URL)
    return session_for_url(LOGISTICS_URL)


def sync_product_to_store(store: Store, product: Product) -> None:
    StoreSession = session_for_url(store.db_url)
    with StoreSession() as session:
        db_prod = session.get(Product, product.id)
        if db_prod:
            db_prod.name = product.name
            db_prod.price = product.price
            db_prod.category = product.category
        else:
            session.add(
                Product(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    category=product.category,
                    stock=product.stock,
                )
            )
        session.commit()


def add_or_update_product(prod: Product) -> Product:
    LogisticsSession = _logistics_session()
    with LogisticsSession() as session:
        session.merge(prod)
        session.commit()
        session.refresh(prod)
        stores: List[Store] = session.query(Store).all()
        for store in stores:
            sync_product_to_store(store, prod)
        return prod


def consolidated_report() -> list[tuple[str, float]]:
    LogisticsSession = _logistics_session()
    totals = []
    with LogisticsSession() as lsession:
        stores = lsession.query(Store).all()
    for store in stores:
        StoreSession = session_for_url(store.db_url)
        with StoreSession() as ssession:
            total = sum(item.price * item.quantity for item in ssession.query(SaleItem).all())
        totals.append((store.name, total))
    return totals

