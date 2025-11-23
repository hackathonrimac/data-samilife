# 🐳 Guía de Docker - Healthcare API

Esta guía explica cómo construir, ejecutar y desplegar la Healthcare API usando Docker.

## 📋 Tabla de Contenidos

- [Requisitos](#requisitos)
- [Construcción](#construcción)
- [Ejecución](#ejecución)
- [Docker Compose](#docker-compose)
- [Producción](#producción)
- [Troubleshooting](#troubleshooting)

---

## Requisitos

- Docker 20.10+
- Docker Compose 2.0+ (opcional)
- 2GB RAM mínimo
- Acceso a una base de datos PostgreSQL

---

## Construcción

### Desarrollo (Dockerfile estándar)

```bash
cd src/backend
docker build -t healthcare-api:dev .
```

### Producción (Multi-stage build)

```bash
cd src/backend
docker build -f Dockerfile.production -t healthcare-api:prod .
```

### Scripts de Ayuda

**Linux/Mac:**
```bash
chmod +x docker-build.sh
./docker-build.sh
```

**Windows:**
```bash
docker-build.bat
```

---

## Ejecución

### Opción 1: Docker Run Simple

```bash
docker run -d \
  --name healthcare-api \
  -p 8000:8000 \
  -e DB_USER=postgres \
  -e DB_PASSWORD=tu_password \
  -e DB_HOST=tu_host \
  -e DB_PORT=5432 \
  -e DB_NAME=healthcare_db \
  healthcare-api:dev
```

### Opción 2: Con archivo .env

1. Crear archivo `.env`:
```env
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=tu_host
DB_PORT=5432
DB_NAME=healthcare_db
```

2. Ejecutar:
```bash
docker run -d \
  --name healthcare-api \
  -p 8000:8000 \
  --env-file .env \
  healthcare-api:dev
```

### Opción 3: Con volumen para logs

```bash
docker run -d \
  --name healthcare-api \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  healthcare-api:dev
```

---

## Docker Compose

Docker Compose facilita la orquestación de múltiples servicios (API + Base de datos).

### Configuración

1. **Copiar archivo de ejemplo:**
```bash
cp .env.docker.example .env
```

2. **Editar `.env` con tus credenciales:**
```env
DB_USER=postgres
DB_PASSWORD=mi_password_seguro
DB_HOST=db
DB_PORT=5432
DB_NAME=healthcare_db
```

### Comandos

**Iniciar servicios:**
```bash
docker-compose up -d
```

**Ver logs:**
```bash
# Todos los servicios
docker-compose logs -f

# Solo API
docker-compose logs -f api

# Solo DB
docker-compose logs -f db
```

**Detener servicios:**
```bash
docker-compose down
```

**Detener y eliminar volúmenes:**
```bash
docker-compose down -v
```

**Reconstruir servicios:**
```bash
docker-compose up -d --build
```

**Ver estado:**
```bash
docker-compose ps
```

### Arquitectura con Docker Compose

```
┌─────────────────────────────────────┐
│         Docker Network              │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │              │  │             │ │
│  │  API         │  │  PostgreSQL │ │
│  │  (Port 8000) │──│  (Port 5432)│ │
│  │              │  │             │ │
│  └──────────────┘  └─────────────┘ │
│         │                           │
└─────────┼───────────────────────────┘
          │
    ┌─────▼─────┐
    │  Logs     │
    │  Volume   │
    └───────────┘
```

---

## Producción

### Dockerfile de Producción

El `Dockerfile.production` usa multi-stage build para optimizar el tamaño:

**Ventajas:**
- ✅ Imagen más pequeña (~200MB vs ~400MB)
- ✅ Sin herramientas de compilación en la imagen final
- ✅ Múltiples workers de Uvicorn
- ✅ Health checks integrados

**Construcción:**
```bash
docker build -f Dockerfile.production -t healthcare-api:1.0.0 .
```

### Variables de Entorno Recomendadas

```env
# Database
DB_USER=postgres
DB_PASSWORD=${SECRET_DB_PASSWORD}
DB_HOST=rds-endpoint.amazonaws.com
DB_PORT=5432
DB_NAME=healthcare_prod

# Application
LOG_LEVEL=WARNING
WORKERS=4
```

### Despliegue en AWS ECS

1. **Construir y subir a ECR:**
```bash
# Login a ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag
docker tag healthcare-api:1.0.0 123456789.dkr.ecr.us-east-1.amazonaws.com/healthcare-api:1.0.0

# Push
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/healthcare-api:1.0.0
```

2. **Crear Task Definition en ECS con:**
   - CPU: 512
   - Memory: 1024
   - Port: 8000
   - Health check: `/health`
   - Environment variables desde Secrets Manager

### Despliegue en Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: healthcare-api
  template:
    metadata:
      labels:
        app: healthcare-api
    spec:
      containers:
      - name: api
        image: healthcare-api:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 40
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 20
          periodSeconds: 10
```

---

## Troubleshooting

### Problema: Contenedor no inicia

**Verificar logs:**
```bash
docker logs healthcare-api
```

**Causas comunes:**
- Variables de entorno faltantes
- Base de datos no accesible
- Puerto 8000 ya en uso

### Problema: No puede conectar a la base de datos

**Verificar conectividad:**
```bash
docker exec -it healthcare-api bash
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
```

**Si usa docker-compose:**
- Asegúrate que `DB_HOST=db` (nombre del servicio)
- Verifica que la DB esté healthy: `docker-compose ps`

### Problema: Health check falla

**Verificar endpoint manualmente:**
```bash
docker exec -it healthcare-api curl http://localhost:8000/health
```

**Verificar estado:**
```bash
docker inspect --format='{{.State.Health.Status}}' healthcare-api
```

### Problema: Permisos de logs

**Cambiar permisos del directorio:**
```bash
sudo chown -R 1000:1000 logs/
```

### Comandos Útiles de Debugging

```bash
# Ver procesos dentro del contenedor
docker exec healthcare-api ps aux

# Ver uso de recursos
docker stats healthcare-api

# Inspeccionar configuración
docker inspect healthcare-api

# Acceder al contenedor
docker exec -it healthcare-api bash

# Ver variables de entorno
docker exec healthcare-api env
```

---

## Mejores Prácticas

### Seguridad

✅ **Hacer:**
- Usar usuario no-root
- Escanear imágenes con `docker scan`
- Usar secrets para credenciales
- Mantener imágenes actualizadas
- Limitar recursos (CPU, memoria)

❌ **No hacer:**
- Incluir `.env` en la imagen
- Correr como root
- Exponer puertos innecesarios
- Usar `latest` en producción

### Performance

- Usar multi-stage builds
- Aprovechar cache de Docker
- Minimizar layers
- Usar `.dockerignore`
- Configurar workers según CPU

### Monitoreo

- Implementar health checks
- Exportar logs a sistema centralizado
- Monitorear métricas de contenedor
- Configurar alertas

---

## Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

---

**Última actualización:** 23 de noviembre de 2025
