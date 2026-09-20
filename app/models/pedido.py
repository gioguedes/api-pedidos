from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.schemas.pedido import StatusPedido


class Base(DeclarativeBase):
    pass


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente: Mapped[str] = mapped_column(String(200), nullable=False)
    produto: Mapped[str] = mapped_column(String(200), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[StatusPedido] = mapped_column(
        SAEnum(StatusPedido), nullable=False, default=StatusPedido.CRIADO
    )
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )