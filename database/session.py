from sqlalchemy.orm import sessionmaker
from database.engine import get_engine

SessionLocal = sessionmaker(
    bind=get_engine(),
    autoflush=False,
    autocommit=False,
    future=True
)


def get_session():
    return SessionLocal()
