"""Business logic for logistics operations (MVC controller)."""

from typing import Optional

from src.db import SessionLocal, init_db, session_for_url
from src.models import Product
from .models import LogisticsStock, RestockRequest, Store


init_db()


def list_stock() -> list[LogisticsStock]:
    with SessionLocal() as session:
        return session.query(LogisticsStock).all()


def register_store(name: str, db_url: str) -> Store:
    with SessionLocal() as session:
        store = Store(name=name, db_url=db_url)
        session.add(store)
        session.commit()
        session.refresh(store)
        return store


def approve_request_by_id(rid: int) -> Optional[RestockRequest]:
    with SessionLocal() as session:
        req = session.get(RestockRequest, rid)
        if not req or req.status != "PENDING":
            return None
        stock = (
            session.query(LogisticsStock)
            .filter_by(product_id=req.product_id)
            .first()
        )
        if not stock or stock.quantity < req.quantity:
            return None
        stock.quantity -= req.quantity
        req.status = "APPROVED"
        session.commit()
        store = session.get(Store, req.store_id)
        if store:
            StoreSession = session_for_url(store.db_url)
            with StoreSession() as s:
                prod = s.get(Product, req.product_id)
                if prod:
                    prod.stock = (prod.stock or 0) + req.quantity
                s.commit()
        return req


def init_logistics_db() -> None:
    __import__("logistics.models")
    init_db()
