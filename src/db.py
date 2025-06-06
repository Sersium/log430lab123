"""
Database engine and session management for POS application.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL from environment or default to PostgreSQL
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg2://postgres:password@localhost:5432/posdb'
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True
)

# Optional second engine used to represent the HQ database. If no separate HQ
# database URL is provided, it defaults to the same engine as the local store.
HQ_DATABASE_URL = os.getenv('HQ_DATABASE_URL')
if HQ_DATABASE_URL:
    hq_engine = create_engine(HQ_DATABASE_URL, echo=False, future=True)
    HQSession = sessionmaker(
        bind=hq_engine, autoflush=False, autocommit=False, future=True
    )
else:
    HQSession = SessionLocal
Base = declarative_base()

def init_db():
    """Create all tables based on ORM models."""
    # Dynamically import models to register them with metadata
    __import__('src.models')
    Base.metadata.create_all(bind=engine)
    if HQ_DATABASE_URL:
        Base.metadata.create_all(bind=hq_engine)
