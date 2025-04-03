# Variables
PROJECT_LABEL = "Cartographie API"
PYTHON_MODULE = "Django_cartographie"  # Doit matcher le nom du dossier principal
PYTHON = python
MANAGE = $(PYTHON) manage.py
TEST_PATH = tests/
COV_PATH = htmlcov/
PYTEST_OPTS = -v -s --ds=config.settings --cov=core --cov=presentation --cov-report term-missing

# Commandes principales
install:
	pip install -r requirements.txt
	
freeze:
	pip freeze > requirements.txt

migrate:
	$(MANAGE) migrate

run:
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
start:
	gunicorn $(PYTHON_MODULE).wsgi:application --bind 0.0.0.0:8000

.PHONY: install migrate run test lint format makemigrations clean start