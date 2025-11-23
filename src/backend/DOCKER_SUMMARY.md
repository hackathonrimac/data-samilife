# 📦 Resumen de Archivos Docker

## Archivos Creados

### 1. **Dockerfile** (Desarrollo)
- Imagen base: `python:3.12-slim`
- Usuario no-root: `appuser`
- Puerto: 8000
- Health check incluido
- Optimizado para desarrollo

**Uso:**
```bash
docker build -t healthcare-api:dev .
docker run -p 8000:8000 --env-file .env healthcare-api:dev
```

---

### 2. **Dockerfile.production** (Producción)
- Multi-stage build
- Imagen optimizada (~200MB)
- 4 workers de Uvicorn
- Health check con curl
- Sin herramientas de compilación en imagen final

**Uso:**
```bash
docker build -f Dockerfile.production -t healthcare-api:prod .
docker run -p 8000:8000 --env-file .env healthcare-api:prod
```

---

### 3. **docker-compose.yml**
Orquesta dos servicios:
- **api**: Healthcare API (FastAPI)
- **db**: PostgreSQL 15

**Características:**
- Red privada entre servicios
- Volumen persistente para PostgreSQL
- Health checks para ambos servicios
- Logs montados como volumen

**Uso:**
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

### 4. **.dockerignore**
Optimiza el build excluyendo:
- `__pycache__/`
- Tests
- Virtual environments
- Archivos de configuración de IDEs
- Logs locales

---

### 5. **.env.docker.example**
Plantilla de variables de entorno para Docker:
```env
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=db
DB_PORT=5432
DB_NAME=healthcare_db
```

**Uso:**
```bash
cp .env.docker.example .env
# Editar .env con tus credenciales
```

---

### 6. **docker-build.sh** (Linux/Mac)
Script de construcción automatizado para sistemas Unix.

**Uso:**
```bash
chmod +x docker-build.sh
./docker-build.sh
```

---

### 7. **docker-build.bat** (Windows)
Script de construcción automatizado para Windows.

**Uso:**
```bash
docker-build.bat
```

---

### 8. **DOCKER.md**
Documentación completa de Docker incluyendo:
- Guía de construcción
- Opciones de ejecución
- Docker Compose
- Despliegue en producción (AWS ECS, Kubernetes)
- Troubleshooting
- Mejores prácticas

---

## Estructura de Archivos

```
src/backend/
├── Dockerfile                  # Imagen de desarrollo
├── Dockerfile.production       # Imagen optimizada para producción
├── docker-compose.yml          # Orquestación de servicios
├── .dockerignore              # Archivos a excluir del build
├── .env.docker.example        # Plantilla de variables de entorno
├── docker-build.sh            # Script de build (Linux/Mac)
├── docker-build.bat           # Script de build (Windows)
├── DOCKER.md                  # Documentación completa
└── DOCKER_SUMMARY.md          # Este archivo
```

---

## Flujo de Trabajo Recomendado

### Desarrollo Local

1. **Construir imagen:**
   ```bash
   docker build -t healthcare-api:dev .
   ```

2. **Ejecutar con docker-compose:**
   ```bash
   cp .env.docker.example .env
   # Editar .env
   docker-compose up -d
   ```

3. **Ver logs:**
   ```bash
   docker-compose logs -f api
   ```

4. **Acceder a la API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

---

### Producción

1. **Construir imagen optimizada:**
   ```bash
   docker build -f Dockerfile.production -t healthcare-api:1.0.0 .
   ```

2. **Probar localmente:**
   ```bash
   docker run -p 8000:8000 --env-file .env healthcare-api:1.0.0
   ```

3. **Subir a registro (ECR, Docker Hub, etc.):**
   ```bash
   docker tag healthcare-api:1.0.0 tu-registro/healthcare-api:1.0.0
   docker push tu-registro/healthcare-api:1.0.0
   ```

4. **Desplegar en plataforma cloud:**
   - AWS ECS
   - Kubernetes
   - Google Cloud Run
   - Azure Container Instances

---

## Comandos Rápidos

```bash
# Construir
docker build -t healthcare-api:dev .

# Ejecutar
docker run -d -p 8000:8000 --env-file .env --name api healthcare-api:dev

# Ver logs
docker logs -f api

# Detener
docker stop api

# Eliminar
docker rm api

# Con docker-compose
docker-compose up -d        # Iniciar
docker-compose logs -f      # Ver logs
docker-compose down         # Detener
docker-compose ps           # Ver estado
```

---

## Verificación

### Health Check

```bash
# Verificar que el contenedor está healthy
docker ps

# Ver detalles del health check
docker inspect --format='{{.State.Health.Status}}' healthcare-api

# Probar endpoint manualmente
curl http://localhost:8000/health
```

### Conectividad a Base de Datos

```bash
# Desde el contenedor
docker exec -it healthcare-api bash
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
```

---

## Recursos

- **Tamaño de imágenes:**
  - Desarrollo: ~400MB
  - Producción: ~200MB

- **Recursos recomendados:**
  - CPU: 0.5-1 vCPU
  - RAM: 512MB-1GB
  - Disco: 1GB

- **Puertos:**
  - API: 8000
  - PostgreSQL: 5432

---

## Notas de Seguridad

✅ **Implementado:**
- Usuario no-root (appuser, UID 1000)
- Variables de entorno para credenciales
- Health checks
- Imagen base oficial de Python
- Dependencias mínimas

⚠️ **Recomendaciones adicionales:**
- Usar secrets manager en producción
- Escanear imágenes regularmente
- Actualizar dependencias
- Implementar rate limiting
- Configurar HTTPS/TLS

---

**Creado:** 23 de noviembre de 2025
**Versión:** 1.0
