# Module defining ORM models for POS application.

"""
ORM models for the POS system.
"""

import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db import Base


class Product(Base):
    """Represents a product in the inventory."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    def __repr__(self):
        return f"<Product {self.name}>"


class Sale(Base):
    """Represents a sale transaction."""

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete")

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
