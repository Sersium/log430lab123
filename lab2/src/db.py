"""
Database engine and session management for POS application.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL from environment or default to PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:password@localhost:5432/posdb",
)


def get_engine(url: str = DATABASE_URL):
    """Return a new SQLAlchemy engine for the given URL."""
    return create_engine(url, echo=False, future=True)


engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def session_for_url(url: str):
    """Return a Session class bound to the specified database URL."""
    eng = get_engine(url)
    return sessionmaker(bind=eng, autoflush=False, autocommit=False, future=True)

def init_db(url: str = DATABASE_URL):
    """Create all tables for the provided database URL."""
    # Dynamically import models to register them with metadata
    __import__("src.models")
    __import__("logistics.models")
    eng = get_engine(url)
    Base.metadata.create_all(bind=eng)
