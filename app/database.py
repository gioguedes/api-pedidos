import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://pedidos:pedidos@localhost:5432/pedidos",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """Fornece uma sessão de banco por requisição (injeção de dependência do FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()