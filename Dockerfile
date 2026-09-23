# Imagem-base: Python enxuto
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências primeiro (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app/ ./app/

EXPOSE 8000

# Comando de inicialização: a mesma imagem pode originar várias instâncias
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]