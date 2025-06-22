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
	$(UV) run pytest $(TEST_PATH)unit/ $(PYTEST_OPTS)

test-unit-auth:
	$(UV) run pytest $(TEST_PATH)unit/auth/ $(PYTEST_OPTS)

test-unit-auth-signup:
	$(UV) run pytest $(TEST_PATH)unit/auth/test_auth_signup_use_case.py $(PYTEST_OPTS)

test-unit-auth-login:
	$(UV) run pytest $(TEST_PATH)unit/auth/test_auth_login_use_case.py $(PYTEST_OPTS)

test-unit-auth-refresh:
	$(UV) run pytest $(TEST_PATH)unit/auth/test_auth_refresh_token_use_case.py $(PYTEST_OPTS)

test-unit-auth-current-user:
	$(UV) run pytest $(TEST_PATH)unit/auth/test_auth_get_current_user_use_case.py $(PYTEST_OPTS)

test-unit-auth-logout:
	$(UV) run pytest $(TEST_PATH)unit/auth/test_auth_logout_use_case.py $(PYTEST_OPTS)

test-unit-city:
	$(UV) run pytest $(TEST_PATH)unit/city/ $(PYTEST_OPTS)

test-unit-city-create:
	$(UV) run pytest $(TEST_PATH)unit/city/test_city_create_use_case.py $(PYTEST_OPTS)

test-unit-city-update:
	$(UV) run pytest $(TEST_PATH)unit/city/test_city_update_use_case.py $(PYTEST_OPTS)

test-unit-city-get:
	$(UV) run pytest $(TEST_PATH)unit/city/test_city_get_use_case.py $(PYTEST_OPTS)

test-unit-city-get-all:
	$(UV) run pytest $(TEST_PATH)unit/city/test_city_get_all_use_case.py $(PYTEST_OPTS)

test-unit-city-delete:
	$(UV) run pytest $(TEST_PATH)unit/city/test_city_delete_use_case.py $(PYTEST_OPTS)

test-unit-city-filter:
	$(UV) run pytest $(TEST_PATH)unit/city/test_city_filter_use_case.py $(PYTEST_OPTS)

test-unit-domain:
	$(UV) run pytest $(TEST_PATH)unit/domain/ $(PYTEST_OPTS)

test-unit-domain-create:
	$(UV) run pytest $(TEST_PATH)unit/domain/test_domain_create_use_case.py $(PYTEST_OPTS)

test-unit-domain-update:
	$(UV) run pytest $(TEST_PATH)unit/domain/test_domain_update_use_case.py $(PYTEST_OPTS)

test-unit-domain-get:
	$(UV) run pytest $(TEST_PATH)unit/domain/test_domain_get_use_case.py $(PYTEST_OPTS)

test-unit-domain-get-all:
	$(UV) run pytest $(TEST_PATH)unit/domain/test_domain_get_all_use_case.py $(PYTEST_OPTS)

test-unit-domain-delete:
	$(UV) run pytest $(TEST_PATH)unit/domain/test_domain_delete_use_case.py $(PYTEST_OPTS)

test-unit-domain-filter:
	$(UV) run pytest $(TEST_PATH)unit/domain/test_domain_filter_use_case.py $(PYTEST_OPTS)

test-unit-establishment-type:
	$(UV) run pytest $(TEST_PATH)unit/establishment_type/ $(PYTEST_OPTS)

test-unit-establishment-type-create:
	$(UV) run pytest $(TEST_PATH)unit/establishment_type/test_establishment_type_create_use_case.py $(PYTEST_OPTS)

test-unit-establishment-type-update:
	$(UV) run pytest $(TEST_PATH)unit/establishment_type/test_establishment_type_update_use_case.py $(PYTEST_OPTS)

test-unit-establishment-type-get:
	$(UV) run pytest $(TEST_PATH)unit/establishment_type/test_establishment_type_get_use_case.py $(PYTEST_OPTS)

test-unit-establishment-type-get-all:
	$(UV) run pytest $(TEST_PATH)unit/establishment_type/test_establishment_type_get_all_use_case.py $(PYTEST_OPTS)

test-unit-establishment-type-delete:
	$(UV) run pytest $(TEST_PATH)unit/establishment_type/test_establishment_type_delete_use_case.py $(PYTEST_OPTS)

test-unit-establishment-type-filter:
	$(UV) run pytest $(TEST_PATH)unit/establishment_type/test_establishment_type_filter_use_case.py $(PYTEST_OPTS)

test-unit-establishment:
	$(UV) run pytest $(TEST_PATH)unit/establishment/ $(PYTEST_OPTS)

test-unit-establishment-create:
	$(UV) run pytest $(TEST_PATH)unit/establishment/test_establishment_create_use_case.py $(PYTEST_OPTS)

test-unit-establishment-get:
	$(UV) run pytest $(TEST_PATH)unit/establishment/test_establishment_get_use_case.py $(PYTEST_OPTS)

test-unit-establishment-update:
	$(UV) run pytest $(TEST_PATH)unit/establishment/test_establishment_update_use_case.py $(PYTEST_OPTS)

test-unit-establishment-delete:
	$(UV) run pytest $(TEST_PATH)unit/establishment/test_establishment_delete_use_case.py $(PYTEST_OPTS)

test-unit-establishment-get-all:
	$(UV) run pytest $(TEST_PATH)unit/establishment/test_establishment_get_all_use_case.py $(PYTEST_OPTS)

test-unit-establishment-filter:
	$(UV) run pytest $(TEST_PATH)unit/establishment/test_establishment_filter_use_case.py $(PYTEST_OPTS)

test-unit-establishment-rate:
	$(UV) run pytest $(TEST_PATH)unit/establishment/test_establishment_rate_use_case.py $(PYTEST_OPTS)

test-e2e:
	$(UV) run pytest $(TEST_PATH)e2e/ $(PYTEST_OPTS)

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
	@echo "  test-unit-auth       - Tests unitaires d'authentification"
	@echo "  test-unit-auth-signup - Tests unitaires signup"
	@echo "  test-unit-auth-login - Tests unitaires login"
	@echo "  test-unit-auth-refresh - Tests unitaires refresh token"
	@echo "  test-unit-auth-current-user - Tests unitaires current user"
	@echo "  test-unit-auth-logout - Tests unitaires logout"
	@echo "  test-unit-city       - Tests unitaires city"
	@echo "  test-unit-city-create - Tests unitaires city create"
	@echo "  test-unit-city-update - Tests unitaires city update"
	@echo "  test-unit-city-get    - Tests unitaires city get"
	@echo "  test-unit-city-get-all - Tests unitaires city get_all"
	@echo "  test-unit-city-delete - Tests unitaires city delete"
	@echo "  test-unit-city-filter - Tests unitaires city filter"
	@echo "  test-unit-domain     - Tests unitaires domain"
	@echo "  test-unit-domain-create - Tests unitaires domain create"
	@echo "  test-unit-domain-update - Tests unitaires domain update"
	@echo "  test-unit-domain-get    - Tests unitaires domain get"
	@echo "  test-unit-domain-get-all - Tests unitaires domain get_all"
	@echo "  test-unit-domain-delete - Tests unitaires domain delete"
	@echo "  test-unit-domain-filter - Tests unitaires domain filter"
	@echo "  test-unit-establishment-type - Tests unitaires establishment_type"
	@echo "  test-unit-establishment-type-create - Tests unitaires establishment_type create"
	@echo "  test-unit-establishment-type-update - Tests unitaires establishment_type update"
	@echo "  test-unit-establishment-type-get    - Tests unitaires establishment_type get"
	@echo "  test-unit-establishment-type-get-all - Tests unitaires establishment_type get_all"
	@echo "  test-unit-establishment-type-delete - Tests unitaires establishment_type delete"
	@echo "  test-unit-establishment-type-filter - Tests unitaires establishment_type filter"
	@echo "  test-unit-establishment - Tests unitaires establishment"
	@echo "  test-unit-establishment-create - Tests unitaires establishment create"
	@echo "  test-unit-establishment-get    - Tests unitaires establishment get"
	@echo "  test-unit-establishment-update - Tests unitaires establishment update"
	@echo "  test-unit-establishment-delete - Tests unitaires establishment delete"
	@echo "  test-unit-establishment-get-all - Tests unitaires establishment get_all"
	@echo "  test-unit-establishment-filter - Tests unitaires establishment filter"
	@echo "  test-unit-establishment-rate - Tests unitaires establishment rate"
	@echo "  test-e2e             - Tests end-to-end"
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

.PHONY: install add-package add-dev-package run start test test-unit test-unit-auth test-unit-auth-signup test-unit-auth-login test-unit-auth-refresh test-unit-auth-current-user test-unit-auth-logout test-unit-city test-unit-city-create test-unit-city-update test-unit-city-get test-unit-city-get-all test-unit-city-delete test-unit-city-filter test-unit-domain test-unit-domain-create test-unit-domain-update test-unit-domain-get test-unit-domain-get-all test-unit-domain-delete test-unit-domain-filter test-unit-establishment-type test-unit-establishment-type-create test-unit-establishment-type-update test-unit-establishment-type-get test-unit-establishment-type-get-all test-unit-establishment-type-delete test-unit-establishment-type-filter test-unit-establishment test-unit-establishment-create test-unit-establishment-get test-unit-establishment-update test-unit-establishment-delete test-unit-establishment-get-all test-unit-establishment-filter test-unit-establishment-rate test-e2e test-repo test-api test-all test-cov test-ci lint format clean shell help docker-start docker-stop docker-restart docker-check-redis docker-check-postgres gen-keys aerich-status aerich-heads aerich-migrate aerich-upgrade aerich-downgrade aerich-history aerich-init aerich-init-db aerich-inspectdb
