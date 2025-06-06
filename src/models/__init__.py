# Module defining ORM models for POS application.

"""
ORM models for the POS system.
"""

import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db import Base


class Store(Base):
    """Represents a physical store location."""

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)

    products = relationship("Product", back_populates="store")
    sales = relationship("Sale", back_populates="store")

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<Store {self.name}>"


class CentralStock(Base):
    """Represents stock kept at the logistics center."""

    __tablename__ = "central_stock"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)

    product = relationship("Product")

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<CentralStock product={self.product_id} qty={self.quantity}>"


class Product(Base):
    """Represents a product in the inventory."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)

    store = relationship("Store", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name}>"


class Sale(Base):
    """Represents a sale transaction."""

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete")

    store = relationship("Store", back_populates="sales")

    def __repr__(self):
        return f"<Sale {self.id}>"


class SaleItem(Base):
    """Represents an item within a sale."""

    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<SaleItem sale={self.sale_id} product={self.product_id}>"
