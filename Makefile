.PHONY: help

.DEFAULT_GOAL := help
THIS_FILE := $(lastword $(MAKEFILE_LIST))

.PHONY: migrate setup-backend setup-frontend 

migrate: ## Run database migrations
	cd backend && \
	. .venv/bin/activate && \
	alembic upgrade head

setup-backend: ## Setup backend dependencies
	cd backend && \
	. .venv/bin/activate && \
	uv sync --frozen

setup-frontend: ## Setup frontend dependencies
	cd frontend && \
	bun install

setup: migrate setup-backend setup-frontend ## Initial project setup (install dependencies, setup database)

.PHONY: db backend frontend dev

db: ## Start database container in detached mode
	docker compose up db -d

backend: ## Start dev server for backend
	cd backend && \
	. .venv/bin/activate && \
	fastapi dev app/main.py

frontend: ## Start dev server for frontend
	cd frontend && \
	bun run dev

dev: ## Start dev servers for all services
	@$(MAKE) -f $(THIS_FILE) db
	@$(MAKE) -f $(THIS_FILE) backend &
	@$(MAKE) -f $(THIS_FILE) frontend


.PHONY: stop-db stop

stop-db: ## Stop database container
	docker compose stop db

stop: stop-db ## Stop all containers

.PHONY: prod stop-prod

prod: ## Build and run production containers
	docker compose -f compose.yaml up -d

stop-prod: ## Stop production containers
	docker compose -f compose.yaml down

help: ## Show this help message
	@echo "CSV Data Ingestion Platform - Development Commands"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)