# Architecture de Test - Guide Complet

Ce document décrit l'architecture et la stratégie de test pour le projet, incluant la résolution du conflit AsyncIO et garantissant la fiabilité, la maintenabilité et l'efficacité du processus de validation du code.

## 1. Objectifs et Problèmes Résolus

### 1.1. Objectifs Principaux

- **Fiabilité :** S'assurer que les nouvelles fonctionnalités n'introduisent pas de régressions.
- **Vitesse :** Permettre une exécution rapide des tests pour un feedback immédiat lors du développement local.
- **Isolation :** Garantir que les tests sont indépendants les uns des autres et de l'environnement extérieur.
- **Reproductibilité :** Assurer que les tests produisent les mêmes résultats quel que soit l'environnement (local, CI/CD).
- **Fidélité :** Permettre l'exécution de tests dans un environnement aussi proche que possible de la production.

### 1.2. Résolution du Conflit AsyncIO

Le principal défi technique résolu dans cette architecture est l'erreur `RuntimeError: Task got Future attached to a different loop`. Cette erreur se produisait car :

- `pytest-asyncio` créait une nouvelle boucle d'événements pour chaque test (`function-scoped`)
- La connexion à la base de données était initialisée une seule fois (`session-scoped`)
- Les opérations de base de données tentaient d'utiliser une boucle d'événements déjà fermée

**Solution :** Utilisation d'une boucle d'événements unique pour toute la session de test combinée à des transactions isolées pour chaque test.

## 2. Structure des Répertoires de Test

Les tests sont organisés en fonction de leur portée et de leur nature pour une meilleure clarté.

### 2.1 Conventions de Nommage des Tests

Pour maintenir une structure de test cohérente et facile à naviguer, nous suivons des conventions de nommage strictes pour les fichiers de test, basées sur le type de test et la couche architecturale ciblée.

| Type de Test | Couche     | Convention de Nommage du Fichier | Exemple                                                                                                              |
| ------------ | ---------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Unitaire     | Repository | `test_repository_name.py`        | [`tests/unit/domain/test_domain_repository.py`](tests/unit/domain/test_domain_repository.py)                         |
| Unitaire     | Use Case   | `test_action_use_case.py`        | [`tests/unit/domain/test_create_domain_use_case.py`](tests/unit/domain/test_create_domain_use_case.py)               |
| Unitaire     | Controller | `test_controller_name.py`        | [`tests/unit/domain/test_domain_controller.py`](tests/unit/domain/test_domain_controller.py)                         |
| Intégration  | Repository | `test_repository_name.py`        | [`tests/integration/domain/test_domain_repository.py`](tests/integration/domain/test_domain_repository.py)           |
| Intégration  | Use Case   | `test_action_use_case.py`        | [`tests/integration/domain/test_create_domain_use_case.py`](tests/integration/domain/test_create_domain_use_case.py) |
| Intégration  | Controller | `test_controller_name.py`        | [`tests/integration/domain/test_domain_controller.py`](tests/integration/domain/test_domain_controller.py)           |
| E2E          | Controller | `test_action_api.py`             | [`tests/e2e/domain/test_create_domain_api.py`](tests/e2e/domain/test_create_domain_api.py)                           |

```
tests/
├── e2e/
│   └── ... (Tests simulant des parcours utilisateurs complets)
├── integration/
│   └── ... (Tests vérifiant l'interaction entre plusieurs composants)
└── unit/
    └── ... (Tests validant un seul composant en isolation)
```

- **`tests/unit`**: Contient les tests unitaires. Ils doivent être rapides et tester une seule unité de code (ex: une fonction, une méthode de cas d'usage) en isolation. Les dépendances externes (base de données, APIs) sont systématiquement mockées. Pour les tests unitaires de cas d'utilisation, la convention est de créer un fichier de test par méthode (ex: [`tests/unit/domain/test_create_domain_use_case.py`](tests/unit/domain/test_create_domain_use_case.py), [`test_update_domain_use_case.py`](tests/unit/domain/test_update_domain_use_case.py), etc.).
  Voici un exemple de structure pour un test unitaire de cas d'utilisation :

```python
# tests/unit/domain/test_create_domain_use_case.py
import pytest
from unittest.mock import AsyncMock

from core.use_cases.domain_use_case import DomainUseCase
from core.entities.domain import DomainEntity
from presentation.exceptions import ConflictException, InternalServerErrorException
from tests.factories import DomainFactory

@pytest.fixture
def mock_domain_repository():
    return AsyncMock()

@pytest.fixture
def domain_use_case(mock_domain_repository):
    return DomainUseCase(domain_repository=mock_domain_repository)

async def test_create_domain_successfully(domain_use_case, mock_domain_repository):
    # Given
    mock_domain_repository.get_by_name.return_value = None
    domain_to_create = DomainFactory.build()
    created_domain_entity = DomainEntity(id=1, **domain_to_create.dict())
    mock_domain_repository.create.return_value = created_domain_entity

    # When
    result = await domain_use_case.create(domain_to_create)

    # Then
    mock_domain_repository.get_by_name.assert_called_once_with(domain_to_create.name)
    mock_domain_repository.create.assert_called_once_with(domain_to_create)
    assert result == created_domain_entity
```

- **`tests/integration`**: Contient les tests d'intégration. Ils vérifient que plusieurs composants interagissent correctement (ex: un cas d'usage avec son implémentation de repository). Ces tests peuvent nécessiter une base de données réelle mais isolée.
- **`tests/e2e` (End-to-End)**: Contient les tests de bout en bout. Ils simulent un parcours utilisateur complet via les points d'entrée de l'application (API REST) et valident le flux jusqu'à la base de données.

## 3. Configuration de `pytest`

`pytest` est le framework de test utilisé pour sa flexibilité et ses puissantes fonctionnalités de fixtures.

### 3.1. Fichier de configuration `pytest.ini`

Un fichier `pytest.ini` à la racine du projet centralise la configuration.

```ini
[pytest]
minversion = 6.0
testpaths = tests
python_files = test_*.py
markers =
    unit: Tests unitaires (rapides, sans I/O)
    integration: Tests d'intégration (avec I/O, ex: BDD)
    e2e: Tests de bout en bout (API -> BDD)
```

- **`testpaths`**: Indique à `pytest` où trouver les tests.
- **`markers`**: Définit des marqueurs personnalisés pour pouvoir exécuter des sous-ensembles de tests (ex: `pytest -m unit`).

### 3.2. Fixtures (`conftest.py`) - Architecture AsyncIO

Les fixtures sont utilisées pour fournir des contextes et des données aux tests de manière modulaire et réutilisable. Le fichier [`tests/conftest.py`](tests/conftest.py) implémente une architecture spécifique pour résoudre les conflits AsyncIO :

#### Fixtures Principales :

- **`event_loop` (scope: "session")** : Crée une boucle `asyncio` unique au début de la session de test et la ferme à la fin. Toutes les opérations asynchrones partagent cette même boucle, éliminant les conflits.

- **`initialize_db` (scope: "session")** : Utilise la boucle d'événements de session pour initialiser la connexion à la base de données de test une seule fois. Utilise les utilitaires de test de `Tortoise ORM` pour créer et détruire automatiquement la base de données de test.

- **`transactional_test` (scope: "function", autouse=True)** : Garantit l'isolation des tests en exécutant chaque test dans une transaction qui est systématiquement annulée (rollback). Cette approche offre :

  - **Isolation Parfaite :** Chaque test s'exécute sur un état de base de données propre
  - **Performance :** Un `ROLLBACK` est beaucoup plus rapide qu'un `TRUNCATE` de table

- **`api_client`** : Fixture qui fournit une instance du `TestClient` de FastAPI pour interroger l'API.

- **Factories** : Utilisation de la librairie `factory-boy` pour générer des données de test cohérentes et réutilisables.

#### Flux Visuel de l'Architecture AsyncIO

```mermaid
graph TB
    subgraph "Début de Session"
        A[pytest démarre] --> B(Création de l'event_loop unique);
        B --> C(Initialisation de la BDD de test);
    end

    subgraph "Exécution de Chaque Test"
        D(Début du test) --> E(Démarrage d'une transaction);
        E --> F(Le test s'exécute...);
        F --> G(Le test modifie la BDD);
        G --> H(Fin du test);
        H --> I(Rollback de la transaction);
    end

    subgraph "Fin de Session"
        J[pytest termine] --> K(Fermeture de l'event_loop);
        K --> L(Suppression de la BDD de test);
    end

    A -- Test 1 --> D;
    I -- Test 2 --> D;
    I -- Fin des tests --> J;
```

## 4. Stratégie de Base de Données et Gestion du Schéma

Pour garantir une isolation et une fidélité maximales, une base de données PostgreSQL dédiée est utilisée pour les tests d'intégration et E2E.

### 4.1. Initialisation de la Base de Données de Test

- **Base de données dédiée** : Une base de données PostgreSQL spécifique, nommée `cartographie_db_test`, est utilisée pour les tests.
- **Cycle de vie isolé** : Cette base de données est créée au début de chaque session de test et supprimée à la fin, assurant une isolation complète entre les exécutions de tests.
- **Fixture `initialize_db`** : La gestion de ce cycle de vie est orchestrée par la fixture `initialize_db` définie dans [`tests/conftest.py`](tests/conftest.py). Cette fixture est responsable de la connexion à la base de données, de sa création, de l'application du schéma, et de sa suppression.

### 4.2. Gestion du Schéma

- **Abandon des migrations `aerich`** : L'utilisation de `aerich` pour les migrations dans l'environnement de test a été abandonnée en raison de problèmes de dépendances et de complexité.
- **Génération directe du schéma** : Le schéma de la base de données est désormais créé directement à partir des modèles Tortoise ORM en utilisant `Tortoise.generate_schemas()`. Cette approche est plus simple, plus rapide et plus robuste pour les tests, car elle garantit que le schéma de la base de données de test correspond toujours aux modèles actuels.

### 4.3. Isolation des Tests

L'isolation des tests est assurée par une approche à deux niveaux :

#### Isolation Principale par BDD Dédiée

L'isolation fondamentale entre les sessions de test est assurée par la création et la suppression d'une base de données de test dédiée à chaque exécution.

#### Isolation Inter-Tests par Transactions

Pour garantir que les tests ne s'influencent pas mutuellement au sein d'une même session, chaque test est exécuté à l'intérieur d'une transaction de base de données qui est systématiquement annulée.

La fixture `transactional_test` (scope: "function", autouse=True) :

- Démarre une nouvelle transaction avant chaque test
- Force une exception après chaque test pour garantir le `ROLLBACK`
- Offre une isolation parfaite avec des performances optimales

### 4.4. Gestion des Erreurs de Base de Données

Les méthodes des repositories doivent intercepter les exceptions spécifiques à la base de données (par exemple, `IntegrityError`, `DoesNotExist` de Tortoise ORM) et les ré-émettre en utilisant les exceptions personnalisées définies dans le domaine (`DatabaseIntegrityException`, `DatabaseDoesNotExistException`, `DatabaseException`). Cette approche garantit que la couche de domaine et les couches supérieures ne dépendent pas des détails d'implémentation de la base de données.

**Exemple de gestion des erreurs dans une méthode `create` de repository :**

```python
from tortoise.exceptions import IntegrityError, DoesNotExist
from core.exceptions import DatabaseIntegrityException, DatabaseDoesNotExistException, DatabaseException
from core.entities.domain import DomainEntity
from apps.tortoise.domain.models import Domain

class DomainRepositoryImpl:
    async def create(self, domain_entity: DomainEntity) -> DomainEntity:
        try:
            domain = await Domain.create(**domain_entity.dict())
            return DomainEntity.from_orm(domain)
        except IntegrityError as e:
            raise DatabaseIntegrityException(message=f"Erreur d'intégrité lors de la création du domaine: {e}", cause=e) from e
        except Exception as e:
            raise DatabaseException(message=f"Erreur inattendue lors de la création du domaine: {e}", cause=e) from e

    async def get_by_name(self, name: str) -> DomainEntity | None:
        try:
            domain = await Domain.get_or_none(name=name)
            return DomainEntity.from_orm(domain) if domain else None
        except DoesNotExist as e:
            raise DatabaseDoesNotExistException(message=f"Le domaine avec le nom '{name}' n'existe pas: {e}", cause=e) from e
        except Exception as e:
            raise DatabaseException(messag=f"Erreur inattendue lors de la récupération du domaine par nom: {e}", cause=e) from e
```

## 5. Exécution des Tests

### 5.1. Commande `make test-int-domain`

La commande `make test-int-domain` est utilisée pour orchestrer le lancement des tests d'intégration spécifiquement pour le module "domain". Cette commande gère l'environnement nécessaire (y compris la base de données de test) et exécute les tests `pytest` pertinents.

```bash
make test-int-domain
```

Cette commande encapsule la logique de démarrage de la base de données de test, de la configuration de l'environnement et de l'exécution des tests d'intégration pour le domaine spécifié.

## 6. Environnement de Test avec Docker Compose

Docker Compose est utilisé pour orchestrer un environnement de test isolé et reproductible.

### 6.1. Fichier `docker-compose.yml`

Le fichier `docker-compose.yml` inclura un service de base de données dédié aux tests.

```yaml
version: "3.8"

services:
  # ... autres services (app, db de dev, etc.)

  test-db:
    image: postgres:13-alpine
    container_name: test_db
    environment:
      - POSTGRES_USER=testuser
      - POSTGRES_PASSWORD=testpass
      - POSTGRES_DB=cartographie_db_test # Nom de la BDD de test
    ports:
      - "5433:5432" # Port différent pour éviter les conflits avec la BDD de dev
    volumes:
      - test_db_data:/var/lib/postgresql/data

  # Le service de l'application peut être réutilisé pour les tests
  # en surchargeant la configuration (ex: DATABASE_URL)
  app:
    build: .
    # ...
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/db # Pour le dev
      # La DATABASE_URL pour les tests sera injectée au moment de l'exécution

volumes:
  test_db_data:
```

### 6.2. Flux d'Exécution des Tests

Pour lancer les tests E2E, on exécute `pytest` à l'intérieur d'un conteneur qui se connecte à `test-db`.

```bash
# Commande pour lancer les tests E2E
docker-compose run --rm -e DATABASE_URL="postgres://testuser:testpass@test-db:5432/cartographie_db_test" app pytest -m "e2e or integration"
```

Cette commande démarre un conteneur `app` éphémère, injecte la variable d'environnement `DATABASE_URL` pour pointer vers la base de données de test, et exécute `pytest`.

## 7. Diagramme de Flux de Test

```mermaid
graph TD
    subgraph "Développeur"
        A[Lancement local: pytest -m unit]
        B[Lancement local: docker-compose run ... pytest -m e2e]
    end

    subgraph "Environnement de Test"
        C{Pytest}
        D[SQLite In-Memory]
        E[Docker Compose]
        F[Conteneur PostgreSQL 'test-db']
        G[Conteneur 'app']
    end

    subgraph "CI/CD (ex: GitHub Actions)"
        H[Workflow CI]
        I[Étape 1: Lancer les tests unitaires]
        J[Étape 2: Lancer les tests E2E & Intégration]
    end

    A --> C -- "Tests unitaires" --> D
    B --> E
    E --> F & G
    G -- "Exécute Pytest" --> C
    C -- "Tests E2E/Intégration" --> F

    H --> I --> C
    H --> J --> E
```

## 8. Avantages de l'Architecture Actuelle

- **Stabilité :** Résout définitivement les erreurs de boucle d'événements AsyncIO
- **Performance :** L'utilisation de transactions pour l'isolation est très rapide
- **Fiabilité :** L'isolation des tests garantit des résultats cohérents
- **Maintenabilité :** L'architecture est alignée sur les meilleures pratiques de `Tortoise ORM` et `pytest`
- **Simplicité :** Abandon des migrations `aerich` complexes au profit de la génération directe du schéma

## 9. Références

- [Tortoise ORM Testing Guide](https://tortoise-orm.readthedocs.io/en/latest/contrib/testing.html)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- Documentation officielle de pytest
- Meilleures pratiques FastAPI pour les tests

## 💡 TL;DR : La Solution AsyncIO

Le conflit `RuntimeError: Task got Future attached to a different loop` est résolu en utilisant une **boucle d'événements `asyncio` unique** pour toute la session de test et en s'assurant que chaque test s'exécute dans une **transaction de base de données isolée** qui est automatiquement annulée (rollback).

Voici le cœur de la solution dans `tests/conftest.py`:

```python
# Une seule boucle d'événements pour toute la session
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Initialisation de la base de données une seule fois
@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_db(event_loop):
    # ... initialisation de Tortoise ...
    yield
    # ... nettoyage de la base de données ...

# Chaque test est enveloppé dans une transaction
@pytest_asyncio.fixture(scope="function", autouse=True)
async def transactional_test():
    async with in_transaction():
        yield
        # Le rollback est forcé pour garantir l'isolation
        # raise Exception("Force rollback")
```
