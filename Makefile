# Variables
PROJECT_LABEL = "Cartographie API"
PYTHON_MODULE = "Django_cartographie"  # Doit matcher le nom du dossier principal
PYTHON = python
MANAGE = $(PYTHON) manage.py
TEST_PATH = tests/
COV_PATH = htmlcov/
PYTEST_OPTS = -v -s --ds=config.settings --cov=core --cov=presentation --cov-report term-missing

# Docker commands
docker-check:
	@echo "Vérification du conteneur Redis..."
	@if ! docker ps | grep -q redis_cartographie; then \
		echo "Le conteneur Redis n'est pas en cours d'exécution. Démarrage..."; \
		docker-compose up -d; \
	else \
		echo "Le conteneur Redis est déjà en cours d'exécution."; \
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

# Modifié pour vérifier et démarrer Redis automatiquement
run: docker-check
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
start: docker-check
	gunicorn $(PYTHON_MODULE).wsgi:application --bind 0.0.0.0:8000

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

.PHONY: install migrate run test lint format makemigrations clean start createapp docker-check docker-start docker-stop docker-restart