# Healthcare API Backend

API backend para búsqueda de establecimientos de salud, citas médicas, precios y medicamentos.

## Estructura del Proyecto

```
src/backend/
├── app/                    # Código de la aplicación
│   ├── db/                # Modelos y conexión a base de datos
│   ├── routes/            # Endpoints de la API
│   ├── services/          # Lógica de negocio
│   ├── schemas/           # Modelos Pydantic
│   ├── utils/             # Utilidades
│   ├── middleware/        # Middleware personalizado
│   ├── logging_config.py  # Configuración de logging
│   └── main.py           # Punto de entrada de la aplicación
├── tests/                 # Tests unitarios y de propiedades
└── logs/                  # Archivos de log (generados automáticamente)
```

## Requisitos

- Python 3.12+
- PostgreSQL
- Dependencias en `requirements.txt`

## Configuración

1. Crear archivo `.env` en la raíz del proyecto con las credenciales de la base de datos:

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=tu_host
DB_PORT=5432
DB_NAME=tu_base_de_datos
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la **raíz del proyecto** (data-samilife/), ejecutar:

```bash
uvicorn src.backend.app.main:app --reload
```

O con configuración personalizada:

```bash
uvicorn src.backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

Documentación interactiva: `http://127.0.0.1:8000/docs`

## Tests

Ejecutar todos los tests desde la raíz del proyecto:

```bash
pytest src/backend/tests/ -v
```

Ejecutar tests específicos:

```bash
# Tests de manejo de errores
pytest src/backend/tests/test_error_handling.py -v

# Tests de servicios
pytest src/backend/tests/test_medication_service.py -v
pytest src/backend/tests/test_pricing_service.py -v

# Tests de utilidades
pytest src/backend/tests/test_schedule_parser.py -v
```

## Endpoints Principales

- `GET /` - Información de la API
- `GET /health` - Health check
- `GET /get` - Buscar establecimientos
- `GET /get/{cod_unico}/informacion` - Información de establecimiento
- `GET /get/{cod_unico}/citas` - Citas disponibles
- `GET /get/precio/cita` - Precio de servicio
- `GET /get/{cod_unico}/farmacos` - Medicamentos disponibles

## Logs

Los logs se generan automáticamente en `src/backend/logs/`:
- `app.log` - Logs generales de la aplicación
- `error.log` - Solo errores

Los logs están en formato JSON estructurado para facilitar el análisis.

---

## 🐳 Docker

### Construcción de la Imagen

**Linux/Mac:**
```bash
cd src/backend
chmod +x docker-build.sh
./docker-build.sh
```

**Windows:**
```bash
cd src/backend
docker-build.bat
```

**Manual:**
```bash
cd src/backend
docker build -t healthcare-api:latest .
```

### Ejecución con Docker

**Opción 1: Docker Run (solo API)**

Crear archivo `.env` en `src/backend/` con las credenciales de la base de datos:
```bash
docker run -p 8000:8000 --env-file .env healthcare-api:latest
```

**Opción 2: Docker Compose (API + PostgreSQL)**

1. Copiar el archivo de ejemplo:
```bash
cp .env.docker.example .env
```

2. Editar `.env` con tus credenciales

3. Iniciar los servicios:
```bash
docker-compose up -d
```

4. Ver logs:
```bash
docker-compose logs -f api
```

5. Detener los servicios:
```bash
docker-compose down
```

### Comandos Útiles de Docker

```bash
# Ver contenedores en ejecución
docker ps

# Ver logs del contenedor
docker logs healthcare-api -f

# Acceder al contenedor
docker exec -it healthcare-api bash

# Detener el contenedor
docker stop healthcare-api

# Eliminar el contenedor
docker rm healthcare-api

# Eliminar la imagen
docker rmi healthcare-api:latest
```

### Estructura de Docker

```
src/backend/
├── Dockerfile              # Definición de la imagen
├── docker-compose.yml      # Orquestación de servicios
├── .dockerignore          # Archivos a ignorar en build
├── .env.docker.example    # Ejemplo de variables de entorno
├── docker-build.sh        # Script de build (Linux/Mac)
└── docker-build.bat       # Script de build (Windows)
```

### Variables de Entorno para Docker

Las siguientes variables deben estar definidas en el archivo `.env`:

```env
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=db                 # 'db' para docker-compose, o IP/hostname para DB externa
DB_PORT=5432
DB_NAME=healthcare_db
```

### Health Check

El contenedor incluye un health check que verifica el endpoint `/health` cada 30 segundos:

```bash
# Ver el estado de salud
docker inspect --format='{{.State.Health.Status}}' healthcare-api
```

### Notas de Producción

- El contenedor corre con un usuario no-root (`appuser`) por seguridad
- Los logs se persisten en un volumen montado
- El health check permite a orquestadores (Kubernetes, ECS) monitorear el estado
- La imagen está optimizada con multi-stage build y cache de dependencias
