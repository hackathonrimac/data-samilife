# Dockerfile para Healthcare API
# Imagen base optimizada con Python 3.12
FROM python:3.12-slim

# Metadata
LABEL maintainer="Healthcare API Team"
LABEL description="FastAPI Healthcare API for establishment search and appointments"
LABEL version="1.0"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/logs && \
    chown -R appuser:appuser /app

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar cache de Docker)
COPY --chown=appuser:appuser requirements.txt .

# Instalar dependencias del sistema necesarias para asyncpg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación (dentro del contexto de build ./backend)
COPY --chown=appuser:appuser app/ ./app/

# Crear directorio para logs
RUN mkdir -p logs && chown -R appuser:appuser logs

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Comando para ejecutar la aplicación (modo auto-reload para desarrollo)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
