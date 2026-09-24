# API de Pedidos Trabalho 1 (Sistemas Distribuídos)

API REST de Pedidos desenvolvida com FastAPI e PostgreSQL, containerizada com Docker.

## Integrantes do grupo

| Nome completo | Turma | RA |
|---|---|---|
| Giovanne Monti Guedes Morgado | CC8P13 | G763289 |
| Isabela Cicilio de Andrade | CC7Q13 | G8694J8 |
| Raphael Della Torre Gimenes | CC8P13 | N202HJ4 |

## Arquitetura

Cliente → API de Pedidos → PostgreSQL

- **Container `pedidos`**: FastAPI com três camadas lógicas API (`app/api`), Service (`app/services`) e Repository (`app/repositories`).
- **Container `postgres`**: banco de dados PostgreSQL 16 com volume persistente.
- Comunicação cliente–API via HTTP/JSON; aplicação–banco via protocolo do PostgreSQL.
- A conexão com o banco é configurada pela variável de ambiente `DATABASE_URL` (ver `.env.example`).

## Como executar

Pré-requisito: Docker Desktop instalado e em execução.

```bash
git clone https://github.com/gioguedes/api-pedidos.git
cd api-pedidos
git checkout APIPedidos-1-final
docker compose up -d --build
```

A API ficará disponível em http://localhost:8000.
Documentação interativa (Swagger): http://localhost:8000/docs

Para encerrar:

```bash
docker compose down        # para os containers (dados permanecem)
docker compose down -v     # para os containers e apaga o volume de dados
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/pedidos` | Cria um pedido (calcula `valor_total` e define status inicial `CRIADO`) |
| GET | `/pedidos/{id}` | Consulta um pedido (200 se existe, 404 se não) |
| GET | `/pedidos` | Lista todos os pedidos |
| PATCH | `/pedidos/{id}/status` | Altera o status (`CRIADO`, `CONFIRMADO`, `CANCELADO`) |
| GET | `/health` | Retorna `{ "status": "ok" }` |

### Transições de status

| Status atual | Pode ir para |
|---|---|
| `CRIADO` | `CONFIRMADO`, `CANCELADO` |
| `CONFIRMADO` | `CANCELADO` |
| `CANCELADO` | — (estado final) |

Transições fora dessa tabela retornam **409 Conflict**.

### Exemplo de criação

```bash
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente": "Giovanne", "produto": "Teclado mecânico", "quantidade": 2, "valor_unitario": 199.90}'
```

Mais exemplos prontos em `docs/requisicoes.http`.

## Estrutura do projeto

```
├── app/
│   ├── main.py                  # inicialização do FastAPI
│   ├── database.py              # configuração da conexão (DATABASE_URL)
│   ├── api/pedidos.py           # endpoints (camada HTTP)
│   ├── services/                # lógica e regras da aplicação
│   ├── repositories/            # persistência (acesso ao banco)
│   ├── models/pedido.py         # modelo persistente (tabela)
│   └── schemas/pedido.py        # entrada e saída da API
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```
