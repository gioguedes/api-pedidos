from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StatusPedido(str, Enum):
    CRIADO = "CRIADO"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"


class PedidoCreate(BaseModel):
    """Dados de entrada para criar um pedido (POST /pedidos)."""

    cliente: str = Field(min_length=1)
    produto: str = Field(min_length=1)
    quantidade: int = Field(gt=0)
    valor_unitario: float = Field(gt=0)


class PedidoStatusUpdate(BaseModel):
    """Dados de entrada para alterar o status (PATCH /pedidos/{id}/status)."""

    status: StatusPedido


class PedidoResponse(BaseModel):
    """Dados de saída da API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: float
    valor_total: float
    status: StatusPedido
    data_criacao: datetime