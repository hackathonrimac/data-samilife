# src/backend/Dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 1. Copiamos requirements desde su ubicación REAL (src/backend/requirements.txt)
COPY src/backend/requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiamos la carpeta 'app' completa
# Esto creará la estructura /app/app/main.py dentro del contenedor
COPY src/backend/app ./app

# Creamos usuario no-root por seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Puerto para App Runner
EXPOSE 8080

# 3. COMANDO DE INICIO AJUSTADO
# Como main.py está dentro del paquete 'app', usamos 'app.main:app'
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]