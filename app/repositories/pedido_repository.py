from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.schemas.pedido import StatusPedido


class PedidoRepository:
    """Abstração das operações de persistência de Pedido."""

    def __init__(self, db: Session):
        self.db = db

    def criar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)  # data_criacao gerados pelo banco
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.get(Pedido, pedido_id)

    def listar(self) -> list[Pedido]:
        return list(self.db.scalars(select(Pedido).order_by(Pedido.id)).all())

    def atualizar_status(self, pedido: Pedido, status: StatusPedido) -> Pedido:
        pedido.status = status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido