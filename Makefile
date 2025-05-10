# Variables
PROJECT_LABEL = "Cartographie API"
PYTHON_MODULE = "Django_cartographie"  # Doit matcher le nom du dossier principal
PYTHON = python
MANAGE = $(PYTHON) manage.py
TEST_PATH = tests/
COV_PATH = htmlcov/
PYTEST_OPTS = -v -s --ds=config.settings --cov=core --cov=presentation --cov-report term-missing


# Génération des clés JWT (privées et publiques)
gen-keys:
	mkdir -p keys
	openssl genrsa -out keys/jwt_access_private.pem 2048
	openssl rsa -in keys/jwt_access_private.pem -pubout -out keys/jwt_access_public.pem
	openssl genrsa -out keys/jwt_refresh_private.pem 2048
	openssl rsa -in keys/jwt_refresh_private.pem -pubout -out keys/jwt_refresh_public.pem

# Création d'un super utilisateur Django
superuser:
	$(MANAGE) createsuperuser

# Docker commands
docker-check:
	@echo "Vérification du conteneur Redis..."
	@if ! docker ps | grep -q redis_cartographie; then \
		echo "Le conteneur Redis n'est pas en cours d'exécution. Démarrage..."; \
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

# Commandes principales
install:
	pip install -r requirements.txt
	
freeze:
	pip freeze > requirements.txt

migrate:
	$(MANAGE) migrate


# Modifié pour vérifier et démarrer Redis et Postgres automatiquement
run: docker-check docker-check-postgres
	$(MANAGE) runserver

test:
	$(MANAGE) test --parallel

# Commandes de test étendues
test-unit:
	pytest $(TEST_PATH)core/ $(PYTEST_OPTS)

test-repo:
	pytest $(TEST_PATH)infrastructure/ $(PYTEST_OPTS)

test-api:
	pytest $(TEST_PATH)presentation/api/ $(PYTEST_OPTS)

test-all:
	pytest $(TEST_PATH) $(PYTEST_OPTS)

test-cov:
	pytest --cov=. --cov-report html && open $(COV_PATH)index.html

test-ci:
	pytest --cov=. --cov-report xml:cov.xml --junitxml=test-results.xml

# Linting et formatage
lint:
	flake8 $(PYTHON_MODULE)
	mypy $(PYTHON_MODULE)
	black --check $(PYTHON_MODULE)

format:
	black $(PYTHON_MODULE)
	isort $(PYTHON_MODULE)

# Création des migrations
makemigrations:
	$(MANAGE) makemigrations

# Nettoyage
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Déploiement local (ex: avec Gunicorn)
start: docker-check docker-check-postgres
	gunicorn $(PYTHON_MODULE).wsgi:application --bind 0.0.0.0:8000

# Environnement virtuel Python
create-venv:
	@if [ ! -d ".venv" ]; then \\
		echo "Création de l'environnement virtuel .venv..."; \\
		$(PYTHON) -m venv .venv; \\
		echo "Environnement virtuel .venv créé."; \\
		echo "Activez-le avec: source .venv/bin/activate"; \\
	else \\
		echo "L'environnement virtuel .venv existe déjà."; \\
	fi

activate-venv:
	@echo "Pour activer l'environnement virtuel, exécutez dans votre terminal :"
	@echo "source .venv/bin/activate"

deactivate-venv:
	@echo "Pour désactiver l'environnement virtuel, exécutez dans votre terminal :"
	@echo "deactivate"

# Création d'une application
createapp:
	@APP_NAME=$(word 2, $(MAKECMDGOALS)) && \
	if [ -z "$$APP_NAME" ]; then \
		echo "Usage: make createapp <app_name>"; \
		exit 1; \
	fi; \
	mkdir -p apps/$$APP_NAME && \
	$(MANAGE) startapp $$APP_NAME apps/$$APP_NAME
	@:

.PHONY: install migrate run test lint format makemigrations clean start createapp docker-check docker-start docker-stop docker-restart gen-keys superuser test-unit test-repo test-api test-all test-cov test-ci create-venv activate-venv deactivate-venv