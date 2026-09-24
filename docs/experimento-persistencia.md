# Experimento: o dado está onde?

Objetivo: verificar onde o estado da aplicação vive quando aplicação e banco executam em containers separados.

## Passos

1. Subir o ambiente:

   ```powershell
   docker compose up -d --build
   ```

2. Criar um pedido pela API:

   ```powershell
   curl.exe -X POST http://localhost:8000/pedidos -H "Content-Type: application/json" -d "{\"cliente\": \"Giovanne\", \"produto\": \"Teclado mecanico\", \"quantidade\": 2, \"valor_unitario\": 199.90}"
   ```

3. Consultar o pedido criado:

   ```powershell
   curl.exe http://localhost:8000/pedidos/1
   ```

4. Reiniciar **somente o container da aplicação**:

   ```powershell
   docker compose restart pedidos
   ```

5. Consultar novamente o mesmo pedido:

   ```powershell
   curl.exe http://localhost:8000/pedidos/1
   ```

## Pergunta

**Por que o dado permaneceu?**

## Resposta

A aplicação de Pedidos é *stateless*: ela não guarda estado. O estado do sistema (os pedidos) está no PostgreSQL, que executa em outro container e grava seus arquivos no volume Docker `dados-postgres`, fora do container da aplicação.

Reiniciar o container `pedidos` apenas recria o processo da API (FastAPI/uvicorn); o volume do banco não é tocado. Por isso o pedido continua disponível após o restart.

O dado só seria apagado com `docker compose down -v`, que remove o volume.