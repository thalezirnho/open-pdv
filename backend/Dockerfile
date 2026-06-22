FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código do backend para o container
COPY . .

# Comando para rodar a aplicação (importante usar --host 0.0.0.0 para aceitar conexões externas ao container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]