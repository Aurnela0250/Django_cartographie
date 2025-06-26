# Patrons de Système : OrientationMada

## Architecture

Le projet OrientationMada est structuré selon les principes de l'Architecture Propre (Clean Architecture), qui vise à séparer les préoccupations et à réduire le couplage entre les différentes parties du système. Cette approche garantit que la logique métier reste indépendante des détails d'implémentation tels que la base de données, le framework web ou les services externes.

L'architecture est divisée en quatre couches principales :

1.  **`core` (Cœur)** :

    - **Description** : La couche la plus interne et la plus indépendante. Elle contient la logique métier fondamentale de l'application.
    - **Composants** :
      - `entities` : Les objets métier qui représentent les concepts clés du domaine (ex: `Establishment`, `Formation`, `User`).
      - `use_cases` : Les cas d'utilisation qui orchestrent les `entities` pour implémenter les fonctionnalités métier.
      - `interfaces` : Les contrats (interfaces ou classes de base abstraites) que les couches externes doivent implémenter (ex: `IUserRepository`, `IEstablishmentRepository`).

2.  **`infrastructure` (Infrastructure)** :

    - **Description** : Implémente les interfaces définies dans la couche `core`. Elle gère les interactions avec les systèmes externes.
    - **Composants** :
      - `db` : L'implémentation des dépôts (repositories) pour l'accès à la base de données, en utilisant Tortoise ORM.
      - `cache` : L'implémentation des services de mise en cache (ex: Redis).
      - `external_services` : Les intégrations avec des services tiers (ex: services de hachage de mots de passe, gestion des JWT).

3.  **`presentation` (Présentation)** :

    - **Description** : La couche la plus externe, responsable de la gestion des interactions avec l'utilisateur (dans ce cas, via une API REST).
    - **Composants** :
      - `api` : Les points de terminaison (endpoints) de l'API, construits avec FastAPI.
      - `schemas` : Les modèles de données (Pydantic) pour la validation et la sérialisation des requêtes et des réponses.
      - `dependencies` : Les dépendances injectées dans les routes FastAPI (ex: authentification, gestion des conteneurs d'injection de dépendances).

4.  **`apps` (Applications)** :
    - **Description** : Contient les modèles de l'ORM Tortoise et les fichiers de migration. Bien que faisant techniquement partie de la couche d'infrastructure, ils sont séparés pour une meilleure organisation.

## Flux de Contrôle

Le flux de contrôle suit la "Règle de Dépendance" : les dépendances ne peuvent pointer que vers l'intérieur.

`Présentation` -> `Cœur` <- `Infrastructure`

- Une requête HTTP arrive à un endpoint dans la couche `presentation`.
- Le endpoint appelle un `use_case` de la couche `core`.
- Le `use_case` utilise les `interfaces` pour interagir avec la base de données ou d'autres services.
- La couche `infrastructure` fournit l'implémentation concrète de ces `interfaces`.
- Le `use_case` retourne le résultat à la couche `presentation`, qui le formate et le renvoie en tant que réponse HTTP.

Ce patron de conception garantit que le système est testable, maintenable et évolutif.

### Gestion des erreurs

Les erreurs sont gérées à l'aide d'exceptions personnalisées dans la couche `core/exceptions.py`. Ces exceptions sont capturées dans les contrôleurs et transformées en réponses HTTP appropriées.

#### Traduction des exceptions d'infrastructure

Un pattern clé est la traduction des exceptions spécifiques de l'infrastructure (comme `tortoise.exceptions.DoesNotExist`) en exceptions applicatives standardisées (comme `NotFoundException`). Cette traduction se produit dans les use cases :

```python
try:
    # Appel au repository
except DatabaseDoesNotExistException as e:
    raise NotFoundException(cause=e)
except DatabaseIntegrityException as e:
    raise ConflictException(cause=e)
except Exception as e:
    raise InternalServerErrorException(cause=e)
```

### Transactions

Les opérations qui modifient plusieurs entités utilisent le décorateur `@atomic` de Tortoise ORM pour garantir l'intégrité des données :

```python
@atomic()
async def update(self, domain_id: int, domain_data: DomainEntity) -> DomainEntity:
    # Logique métier
```

### Tests unitaires

L'approche TDD est strictement suivie avec :

- Mocking des repositories avec `unittest.mock.Mock(spec=IDomainRepository)`
- Vérification des appels attendus aux méthodes du repository
- Tests des cas limites et de gestion d'erreurs
- Utilisation de `AsyncMock` pour les méthodes asynchrones

---

### [2025-06-24] - Convention de Test

#### Structure des Tests

- **Arrange/Act/Assert** : Chaque test suit ce modèle pour une lisibilité et une maintenance claires.
- **Classes Imbriquées** : Les cas de test sont organisés en classes `TestSuccess` et `TestFailures` pour séparer les scénarios de réussite et d'échec.

#### Configuration des Tests

- **`conftest.py` Local** : Chaque module de test peut avoir son propre `conftest.py` pour les fixtures locales, favorisant l'encapsulation.
- **`Makefile`** : Un `Makefile` centralise les commandes de test, simplifiant l'exécution des tests (`make test`, `make test-unit`, `make test-integration`).
