# Makefile para Healthcare API
# Simplifica comandos comunes de Docker y desarrollo

.PHONY: help build build-prod run run-prod stop clean logs test shell db-shell compose-up compose-down compose-logs

# Variables
IMAGE_NAME = healthcare-api
IMAGE_TAG = dev
PROD_TAG = prod
CONTAINER_NAME = healthcare-api
COMPOSE_FILE = docker-compose.yml

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(GREEN)Healthcare API - Comandos disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================
# Docker Build
# ============================================

build: ## Construir imagen de desarrollo
	@echo "$(GREEN)Construyendo imagen de desarrollo...$(NC)"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "$(GREEN)✅ Imagen construida: $(IMAGE_NAME):$(IMAGE_TAG)$(NC)"

build-prod: ## Construir imagen de producción (optimizada)
	@echo "$(GREEN)Construyendo imagen de producción...$(NC)"
	docker build -f Dockerfile.production -t $(IMAGE_NAME):$(PROD_TAG) .
	@echo "$(GREEN)✅ Imagen construida: $(IMAGE_NAME):$(PROD_TAG)$(NC)"

# ============================================
# Docker Run
# ============================================

run: ## Ejecutar contenedor de desarrollo
	@echo "$(GREEN)Iniciando contenedor...$(NC)"
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		--env-file .env \
		-v $(PWD)/logs:/app/logs \
		$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "$(GREEN)✅ Contenedor iniciado: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Docs: http://localhost:8000/docs$(NC)"

run-prod: ## Ejecutar contenedor de producción
	@echo "$(GREEN)Iniciando contenedor de producción...$(NC)"
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		--env-file .env \
		-v $(PWD)/logs:/app/logs \
		$(IMAGE_NAME):$(PROD_TAG)
	@echo "$(GREEN)✅ Contenedor iniciado: http://localhost:8000$(NC)"

stop: ## Detener contenedor
	@echo "$(YELLOW)Deteniendo contenedor...$(NC)"
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	@echo "$(GREEN)✅ Contenedor detenido$(NC)"

# ============================================
# Docker Compose
# ============================================

compose-up: ## Iniciar servicios con docker-compose (API + DB)
	@echo "$(GREEN)Iniciando servicios con docker-compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Servicios iniciados$(NC)"
	@echo "$(YELLOW)API: http://localhost:8000$(NC)"
	@echo "$(YELLOW)DB: localhost:5432$(NC)"

compose-down: ## Detener servicios de docker-compose
	@echo "$(YELLOW)Deteniendo servicios...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

compose-logs: ## Ver logs de docker-compose
	docker-compose logs -f

compose-restart: ## Reiniciar servicios de docker-compose
	@echo "$(YELLOW)Reiniciando servicios...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✅ Servicios reiniciados$(NC)"

# ============================================
# Utilidades
# ============================================

logs: ## Ver logs del contenedor
	docker logs -f $(CONTAINER_NAME)

shell: ## Acceder al shell del contenedor
	docker exec -it $(CONTAINER_NAME) bash

db-shell: ## Acceder al shell de PostgreSQL (docker-compose)
	docker-compose exec db psql -U $$DB_USER -d $$DB_NAME

ps: ## Ver estado de contenedores
	@echo "$(GREEN)Contenedores en ejecución:$(NC)"
	@docker ps -a | grep $(IMAGE_NAME) || echo "$(YELLOW)No hay contenedores de $(IMAGE_NAME)$(NC)"

health: ## Verificar health check
	@echo "$(GREEN)Estado de salud:$(NC)"
	@docker inspect --format='{{.State.Health.Status}}' $(CONTAINER_NAME) 2>/dev/null || echo "$(RED)Contenedor no encontrado$(NC)"

# ============================================
# Testing
# ============================================

test: ## Ejecutar tests dentro del contenedor
	docker exec $(CONTAINER_NAME) pytest tests/ -v

test-local: ## Ejecutar tests localmente (sin Docker)
	pytest tests/ -v

# ============================================
# Limpieza
# ============================================

clean: ## Limpiar contenedores e imágenes
	@echo "$(YELLOW)Limpiando contenedores e imágenes...$(NC)"
	docker stop $(CONTAINER_NAME) 2>/dev/null || true
	docker rm $(CONTAINER_NAME) 2>/dev/null || true
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	docker rmi $(IMAGE_NAME):$(PROD_TAG) 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

clean-all: ## Limpieza completa (incluye volúmenes)
	@echo "$(RED)⚠️  Limpieza completa (incluye volúmenes)...$(NC)"
	docker-compose down -v
	docker stop $(CONTAINER_NAME) 2>/dev/null || true
	docker rm $(CONTAINER_NAME) 2>/dev/null || true
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	docker rmi $(IMAGE_NAME):$(PROD_TAG) 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza completa$(NC)"

# ============================================
# Desarrollo
# ============================================

dev: build run ## Build y run en un solo comando
	@echo "$(GREEN)✅ Entorno de desarrollo listo$(NC)"

dev-compose: compose-up ## Iniciar entorno completo (API + DB)
	@echo "$(GREEN)✅ Entorno completo listo$(NC)"

restart: stop run ## Reiniciar contenedor
	@echo "$(GREEN)✅ Contenedor reiniciado$(NC)"

# ============================================
# Información
# ============================================

info: ## Mostrar información del sistema
	@echo "$(GREEN)Información del sistema:$(NC)"
	@echo "  Docker version: $$(docker --version)"
	@echo "  Docker Compose version: $$(docker-compose --version)"
	@echo ""
	@echo "$(GREEN)Imágenes:$(NC)"
	@docker images | grep $(IMAGE_NAME) || echo "  $(YELLOW)No hay imágenes de $(IMAGE_NAME)$(NC)"
	@echo ""
	@echo "$(GREEN)Contenedores:$(NC)"
	@docker ps -a | grep $(IMAGE_NAME) || echo "  $(YELLOW)No hay contenedores de $(IMAGE_NAME)$(NC)"

# Default target
.DEFAULT_GOAL := help
