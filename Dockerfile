FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para pymssql
RUN apt-get update && apt-get install -y \
    freetds-dev \
    freetds-bin \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicacion
COPY . .

# Exponer puerto
EXPOSE 8080

# Comando para iniciar
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
