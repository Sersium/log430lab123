"""Models for the logistics service."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db import Base

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    db_url = Column(String, nullable=False)

class LogisticsStock(Base):
    __tablename__ = "logistics_stock"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")

class RestockRequest(Base):
    __tablename__ = "restock_requests"
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="PENDING")

    store = relationship("Store")
    product = relationship("Product")
