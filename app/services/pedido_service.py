from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.pedido import PedidoCreate, StatusPedido


class PedidoNaoEncontradoError(Exception):
    """Lançado quando o pedido não existe; a camada de API traduz para 404."""


class TransicaoStatusInvalidaError(Exception):
    """Lançado quando a mudança de status não é permitida; a camada de API traduz para 409."""

    def __init__(self, atual: StatusPedido, novo: StatusPedido):
        super().__init__(f"Transição de status inválida: {atual.value} -> {novo.value}")


# Regra de negócio: transições de status permitidas (CANCELADO é estado final)
TRANSICOES_PERMITIDAS: dict[StatusPedido, set[StatusPedido]] = {
    StatusPedido.CRIADO: {StatusPedido.CONFIRMADO, StatusPedido.CANCELADO},
    StatusPedido.CONFIRMADO: {StatusPedido.CANCELADO},
    StatusPedido.CANCELADO: set(),
}


class PedidoService:
    """Concentra a lógica da aplicação e coordena as operações."""

    def __init__(self, db: Session):
        self.repository = PedidoRepository(db)

    def criar_pedido(self, dados: PedidoCreate) -> Pedido:
        pedido = Pedido(
            cliente=dados.cliente,
            produto=dados.produto,
            quantidade=dados.quantidade,
            valor_unitario=dados.valor_unitario,
            # Regra de negócio: a aplicação calcula o valor total
            valor_total=round(dados.quantidade * dados.valor_unitario, 2),
            # Regra de negócio: a aplicação define o status inicial
            status=StatusPedido.CRIADO,
        )
        return self.repository.criar(pedido)

    def consultar_pedido(self, pedido_id: int) -> Pedido:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido is None:
            raise PedidoNaoEncontradoError(pedido_id)
        return pedido

    def listar_pedidos(self) -> list[Pedido]:
        return self.repository.listar()

    def alterar_status(self, pedido_id: int, status: StatusPedido) -> Pedido:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido is None:
            raise PedidoNaoEncontradoError(pedido_id)
        if status not in TRANSICOES_PERMITIDAS[pedido.status]:
            raise TransicaoStatusInvalidaError(pedido.status, status)
        return self.repository.atualizar_status(pedido, status)