import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.api.pedidos import router as pedidos_router
from app.database import engine
from app.models.pedido import Base


def criar_tabelas(tentativas: int = 10, espera_segundos: int = 3) -> None:
    """Cria as tabelas no banco, aguardando o PostgreSQL ficar pronto."""
    for tentativa in range(1, tentativas + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if tentativa == tentativas:
                raise
            time.sleep(espera_segundos)


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(title="API de Pedidos", version="1.0.0", lifespan=lifespan)
app.include_router(pedidos_router)


@app.get("/health")
def health():
    return {"status": "ok"}