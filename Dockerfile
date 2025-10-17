# Dockerfile
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os requisitos (necessário para o confluent-kafka)
COPY requirements.txt .

# Instala as dependências, incluindo as do OS para o confluent-kafka (librdkafka)
# Este é um passo crítico para a instalação do confluent-kafka em ambientes Alpine/slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsasl2-dev \
    libssl-dev \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia os scripts e a API
COPY producer.py consumer.py api.py .

# A porta que a API Flask/FastAPI irá expor
EXPOSE 5000 

# Comando para iniciar a API (usando gunicorn para produção simples)
# Usaremos um comando de inicialização simples
CMD ["python", "api.py"]