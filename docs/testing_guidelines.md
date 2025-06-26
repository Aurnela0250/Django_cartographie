# Guide des Tests (Unitaires, Intégration et E2E)

Ce document établit les conventions et les meilleures pratiques pour la rédaction des tests (unitaires, intégration et End-to-End) dans ce projet. L'objectif est de garantir la cohérence, la maintenabilité et la fiabilité de notre suite de tests.

## 1. Configuration de Base des Tests

La configuration des tests repose sur deux fichiers principaux qui fournissent les outils et les données nécessaires à l'ensemble de la suite de tests.

### 1.1. Fixtures Globales : [`tests/conftest.py`](tests/conftest.py:1)

Le fichier [`tests/conftest.py`](tests/conftest.py:1) est central pour la configuration des tests Pytest. Il fournit des fixtures essentielles qui gèrent :

- **L'initialisation de la base de données** (`initialize_db`) pour garantir un environnement propre à chaque session de test d'intégration et E2E.
- **L'instance de l'application FastAPI** (`app`) pour les tests d'intégration et E2E.
- **Le client HTTP asynchrone** (`authenticated_async_client`) pour effectuer des requêtes authentifiées vers l'API dans les tests E2E.

### 1.2. Génération de Données : [`tests/factories.py`](tests/factories.py:1)

Le fichier [`tests/factories.py`](tests/factories.py:1) utilise la bibliothèque `polyfactory` pour générer des données de test réalistes et valides pour les entités et les schémas Pydantic de l'application.

L'utilisation de ces factories (ex: `CreateDomainSchemaFactory`, `DomainEntityFactory`) est cruciale pour construire les payloads et les entités, ce qui évite le codage en dur et rend les tests plus robustes aux changements de modèles.

## 2. Tests Unitaires

Les tests unitaires valident une seule unité de logique (un cas d'usage) de manière isolée, sans dépendances externes comme une base de données.

### 2.1. Conventions

- **Nommage des Fichiers** : Chaque fichier de test unitaire doit correspondre à un cas d'usage spécifique et suivre le pattern `test_{action}_{entité}_use_case.py` (e.g., `test_create_level_use_case.py`).
- **Pattern Arrange/Act/Assert (Given/When/Then)** : Chaque test doit être divisé en trois sections claires.
- **Classes de Test Imbriquées** : Utilisez des classes comme `TestSuccess` et `TestFailures` pour regrouper les scénarios.
- **Injection de Mocks** : Les dépendances (repositories) sont mockées et injectées via des fixtures pytest définies dans un `conftest.py` local au module (e.g., [`tests/unit/domain/conftest.py`](tests/unit/domain/conftest.py:1)).

### 2.2. Exemple de Test Unitaire

Voici un exemple tiré de [`tests/unit/domain/test_update_domain_use_case.py`](tests/unit/domain/test_update_domain_use_case.py:1).

```python
# tests/unit/domain/test_update_domain_use_case.py
import pytest
from core.entities.domain import DomainEntity
from presentation.exceptions import NotFoundException

class TestUpdateDomainUseCase:
    class TestSuccess:
        async def test_update_domain_success(
            self, domain_use_case, mock_domain_repository
        ):
            # Arrange (Given)
            domain_id = 1
            user_id = 1
            domain_data = {"name": "Updated Domain"}
            existing_domain = DomainEntity(id=domain_id, name="Original Domain")
            updated_domain = DomainEntity(id=domain_id, name="Updated Domain", updated_by=user_id)
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.update.return_value = updated_domain

            # Act (When)
            result = await domain_use_case.update(domain_id, domain_data, user_id)

            # Assert (Then)
            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.update.assert_called_once()
            assert result == updated_domain
```

## 3. Tests d'Intégration

Les tests d'intégration vérifient que les composants interagissent correctement avec la base de données.

### 3.1. Conventions

- **Interaction Base de Données** : Ces tests effectuent des opérations CRUD réelles.
- **Isolation** : La fixture `initialize_db` garantit que la base de données est propre pour chaque session de test.
- **Marqueur Pytest** : Marquez les tests avec `@pytest.mark.integration`.

### 3.2. Exemple de Test d'Intégration

Voici un exemple de [`tests/integration/domain/test_create_domain_repository.py`](tests/integration/domain/test_create_domain_repository.py).

```python
# tests/integration/domain/test_create_domain_repository.py
import pytest
from core.container import Container
from core.interfaces.domain_repository import IDomainRepository
from tests.factories import DomainEntityFactory, UserEntityFactory

pytestmark = pytest.mark.integration

async def test_create_and_get_domain(container: Container):
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()
    user_repository = container.user_repository()
    user = await user_repository.create(UserEntityFactory.build())
    domain_entity = DomainEntityFactory.build(created_by=user.id, updated_by=user.id)

    # Act
    created_domain = await domain_repository.create(domain_entity)
    retrieved_domain = await domain_repository.get(created_domain.id)

    # Assert
    assert retrieved_domain is not None
    assert retrieved_domain.id == created_domain.id
    assert retrieved_domain.name == domain_entity.name
```

## 4. Tests End-to-End (E2E)

Les tests E2E simulent un parcours utilisateur complet en effectuant des requêtes HTTP sur les endpoints de l'API.

### 4.1. Conventions

- **Client HTTP** : Utilisez la fixture `authenticated_async_client` pour les requêtes authentifiées.
- **Assertions** : Vérifiez le code de statut HTTP et le contenu de la réponse JSON.
- **Marqueur Pytest** : Marquez les tests avec `@pytest.mark.e2e`.

### 4.2. Exemple de Test E2E

Voici un exemple de [`tests/e2e/domain/test_create_domain_controller.py`](tests/e2e/domain/test_create_domain_controller.py).

```python
# tests/e2e/domain/test_create_domain_controller.py
import pytest
from httpx import AsyncClient
from tests.factories import CreateDomainSchemaFactory

pytestmark = pytest.mark.e2e

async def test_create_domain_success(authenticated_async_client: AsyncClient):
    # Arrange
    domain_data = CreateDomainSchemaFactory.build()

    # Act
    response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain_data.model_dump(),
    )

    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert isinstance(response_data["id"], int)
    assert response_data["name"] == domain_data.name
```

## 5. Gestion et Exécution des Tests via le Makefile

Pour garantir une exécution cohérente, toutes les commandes de test doivent être définies et exécutées via le [`Makefile`](Makefile).

### 5.1. Ajout de Nouveaux Scripts de Test

**Règle :** Pour chaque nouveau fichier de test (unitaire, intégration ou E2E), une entrée correspondante **doit** être ajoutée au [`Makefile`](Makefile).

Exemple d'ajout :

```makefile
# Pour un test unitaire
test-unit-domain-update:
	$(UV) run pytest $(TEST_PATH)unit/domain/test_update_domain_use_case.py $(PYTEST_OPTS)

# Pour un test d'intégration
test-int-domain-create: docker-check-postgres
	$(UV) run pytest $(TEST_PATH)integration/domain/test_create_domain_repository.py $(PYTEST_OPTS)

# Pour un test E2E
test-e2e-domain-create: docker-check-postgres
	$(UV) run pytest $(TEST_PATH)e2e/domain/test_create_domain_controller.py $(PYTEST_OPTS)
```

### 5.2. Exécution des Tests

L'exécution des tests **doit** se faire via les commandes `make`.

- **Exécuter tous les tests :**
  ```bash
  make test
  ```
- **Exécuter un groupe de tests (ex: tous les tests unitaires) :**
  ```bash
  make test-unit
  ```
- **Exécuter un test spécifique :**
  ```bash
  make test-unit-domain-update
  ```
