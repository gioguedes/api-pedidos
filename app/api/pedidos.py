from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoStatusUpdate
from app.services.pedido_service import (
    PedidoNaoEncontradoError,
    PedidoService,
    TransicaoStatusInvalidaError,
)

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    return PedidoService(db).criar_pedido(dados)


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return PedidoService(db).listar_pedidos()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        return PedidoService(db).consultar_pedido(pedido_id)
    except PedidoNaoEncontradoError:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def alterar_status(pedido_id: int, dados: PedidoStatusUpdate, db: Session = Depends(get_db)):
    try:
        return PedidoService(db).alterar_status(pedido_id, dados.status)
    except PedidoNaoEncontradoError:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    except TransicaoStatusInvalidaError as erro:
        raise HTTPException(status_code=409, detail=str(erro))