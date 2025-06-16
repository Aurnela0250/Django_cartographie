# Variables
PROJECT_LABEL = "Cartographie API FastAPI"
PROJECT_MODULE = "main"
UV = uv
TEST_PATH = tests/
COV_PATH = htmlcov/
PYTEST_OPTS = -v -s --cov=core --cov=presentation --cov-report term-missing

# Génération des clés JWT (privées et publiques)
gen-keys:
	mkdir -p keys
	openssl genrsa -out keys/jwt_access_private.pem 2048
	openssl rsa -in keys/jwt_access_private.pem -pubout -out keys/jwt_access_public.pem
	openssl genrsa -out keys/jwt_refresh_private.pem 2048
	openssl rsa -in keys/jwt_refresh_private.pem -pubout -out keys/jwt_refresh_public.pem

# Docker commands
docker-check-redis:
	@echo "Vérification du conteneur Redis..."
	@if ! docker ps | grep -q redis_cartographie; then \
		echo "Le conteneur Redis n'est pas en cours d'exécution. Démarrage..."; \
		echo "Démarrage des services avec .env..."; \
		docker-compose up -d; \
	else \
		echo "Le conteneur Redis est déjà en cours d'exécution."; \
	fi

docker-check-postgres:
	@echo "Vérification du conteneur Postgres..."
	@if ! docker ps | grep -q postgres_cartographie; then \
		echo "Le conteneur Postgres n'est pas en cours d'exécution. Démarrage..."; \
		docker-compose up -d; \
	else \
		echo "Le conteneur Postgres est déjà en cours d'exécution."; \
	fi

docker-start:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-restart:
	docker-compose restart

# Commandes principales avec UV
install:
	$(UV) sync
	
add-package:
	@PACKAGE=$(word 2, $(MAKECMDGOALS)) && \
	if [ -z "$$PACKAGE" ]; then \
		echo "Usage: make add-package <package_name>"; \
		exit 1; \
	fi; \
	$(UV) add $$PACKAGE
	@:

add-dev-package:
	@PACKAGE=$(word 2, $(MAKECMDGOALS)) && \
	if [ -z "$$PACKAGE" ]; then \
		echo "Usage: make add-dev-package <package_name>"; \
		exit 1; \
	fi; \
	$(UV) add --dev $$PACKAGE
	@:

# FastAPI Server
run: docker-check-redis docker-check-postgres
	$(UV) run fastapi dev

# Production server
start: docker-check-redis docker-check-postgres
	$(UV) run fastapi run --host 0.0.0.0 --port 8000

# Commandes de test avec UV
test:
	$(UV) run pytest

test-unit:
	$(UV) run pytest $(TEST_PATH)core/ $(PYTEST_OPTS)

test-repo:
	$(UV) run pytest $(TEST_PATH)infrastructure/ $(PYTEST_OPTS)

test-api:
	$(UV) run pytest $(TEST_PATH)presentation/api/ $(PYTEST_OPTS)

test-all:
	$(UV) run pytest $(TEST_PATH) $(PYTEST_OPTS)

test-cov:
	$(UV) run pytest --cov=. --cov-report html && open $(COV_PATH)index.html

test-ci:
	$(UV) run pytest --cov=. --cov-report xml:cov.xml --junitxml=test-results.xml

# Linting et formatage avec UV
lint:
	$(UV) run ruff check .
	$(UV) run mypy .
	$(UV) run black --check .

format:
	$(UV) run black .
	$(UV) run ruff format .
	$(UV) run ruff check . --fix

# Commandes Aerich pour Tortoise ORM
aerich-status:
	@echo "🔍 Migration Status (Aerich)"
	@echo "=========================="
	$(UV) run aerich status

aerich-heads:
	@echo "🤕 Current Migration Heads (Aerich)"
	@echo "=================================="
	$(UV) run aerich heads

aerich-migrate:
	@MESSAGE=$(word 2, $(MAKECMDGOALS)) && \
	if [ -z "$$MESSAGE" ]; then \
		echo "Usage: make aerich-migrate \"message\""; \
		exit 1; \
	fi; \
	echo "🔨 Creating migration (Aerich): $$MESSAGE"; \
	$(UV) run aerich migrate --name "$$MESSAGE"
	@:

aerich-upgrade:
	@echo "🚀 Applying migrations (Aerich)..."
	$(UV) run aerich upgrade

aerich-downgrade:
	@echo "⏪ Rolling back last migration (Aerich)..."
	@echo "Current status:"
	$(UV) run aerich status
	@read -p "⚠️  Are you sure you want to rollback? (y/N): " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(UV) run aerich downgrade -1; \
	else \
		echo "❌ Rollback cancelled"; \
	fi

aerich-history:
	@echo "📜 Migration History (Aerich)"
	@echo "============================"
	$(UV) run aerich history

aerich-init:
	@echo "⚙️  Initializing Aerich configuration..."
	$(UV) run aerich init -t config.settings.TORTOISE_ORM
	@echo "✅ Aerich configuration initialized. Review pyproject.toml or aerich.ini."

aerich-init-db:
	@echo "🚀 Initializing creating initial migration..."
	$(UV) run aerich init-db
	@echo "✅ Aerich initialized and initial migration created. Run 'make aerich-upgrade' to apply."

aerich-inspectdb:
	@echo "🔍 Inspecting database (Aerich)..."
	$(UV) run aerich inspectdb

# Nettoyage
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Scripts utilitaires
shell:
	$(UV) run python

# Aide
help:
	@echo "Commandes disponibles:"
	@echo "====================="
	@echo "Gestion des dépendances:"
	@echo "  install              - Installer les dépendances"
	@echo "  add-package          - Ajouter un package"
	@echo "  add-dev-package      - Ajouter un package de développement"
	@echo ""
	@echo "Serveur FastAPI:"
	@echo "  run                  - Lancer le serveur de développement"
	@echo "  start                - Lancer le serveur de production"
	@echo ""
	@echo "Tests:"
	@echo "  test                 - Lancer tous les tests"
	@echo "  test-unit            - Tests unitaires"
	@echo "  test-api             - Tests API"
	@echo "  test-cov             - Tests avec couverture"
	@echo ""
	@echo "Migrations Aerich (Tortoise ORM):"
	@echo "  aerich-status        - Voir l'état des migrations"
	@echo "  aerich-migrate       - Créer une nouvelle migration (ex: make aerich-migrate \"add_user_table\")"
	@echo "  aerich-upgrade       - Appliquer les migrations"
	@echo "  aerich-downgrade     - Revenir en arrière sur la dernière migration"
	@echo "  aerich-history       - Historique des migrations"
	@echo "  aerich-heads         - Afficher les têtes de migration actuelles"
	@echo "  aerich-init          - Initialiser la configuration Aerich (crée/met à jour la config)"
	@echo "  aerich-init-db       - Générer le schéma initial et le dossier de migration des applications"
	@echo "  aerich-inspectdb     - Inspecter la base de données et générer les modèles Tortoise ORM"
	@echo ""
	@echo "Docker:"
	@echo "  docker-start         - Démarrer les services Docker"
	@echo "  docker-stop          - Arrêter les services Docker"
	@echo ""
	@echo "Utilitaires:"
	@echo "  lint                 - Vérifier le code"
	@echo "  format               - Formater le code"
	@echo "  clean                - Nettoyer les fichiers Python"
	@echo "  gen-keys             - Générer les clés JWT"

.PHONY: install add-package add-dev-package run start test test-unit test-repo test-api test-all test-cov test-ci lint format clean shell help docker-start docker-stop docker-restart docker-check-redis docker-check-postgres gen-keys aerich-status aerich-heads aerich-migrate aerich-upgrade aerich-downgrade aerich-history aerich-init aerich-init-db aerich-inspectdb