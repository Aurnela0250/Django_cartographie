# Tests du Projet

Ce dossier contient les tests pour le projet, organisés selon une architecture en couches.

## Structure des tests

```
tests/
├── unit/                      # Tests unitaires isolés
│   ├── core/                  # Tests du cœur métier
│   │   └── use_cases/         # Tests des cas d'utilisation
│   └── presentation/          # Tests des contrôleurs et schémas
│       ├── api/
│       └── schemas/
├── integration/               # Tests d'intégration
│   └── repositories/          # Tests avec base de données réelle
└── api/                       # Tests complets des endpoints
    └── v1/                    # Tests par version d'API
```

## Exécution des tests

Vous pouvez exécuter les tests avec les commandes suivantes :

```bash
# Tous les tests
pytest

# Tests unitaires uniquement
pytest tests/unit/

# Tests d'intégration uniquement
pytest tests/integration/

# Tests d'API uniquement
pytest tests/api/

# Tests avec couverture de code
pytest --cov=.

# Générer un rapport de couverture HTML
pytest --cov=. --cov-report=html
```

## Marqueurs de tests

Les tests sont marqués pour faciliter leur exécution sélective :

```bash
# Exécuter uniquement les tests unitaires
pytest -m unit

# Exécuter uniquement les tests d'intégration
pytest -m integration

# Exécuter uniquement les tests d'API
pytest -m api
```

## Fixtures communes

Des fixtures communes sont définies dans le fichier `conftest.py` et peuvent être utilisées dans tous les tests :

- `user_repository` : Une instance de DjangoUserRepository
- `jwt_service` : Une instance de JWTService
- `test_user` : Un utilisateur de test créé dans la base de données
- `test_user_entity` : Une entité utilisateur de test (sans sauvegarde en base)
- `auth_tokens` : Des jetons d'authentification pour un utilisateur de test
- `auth_header` : Un en-tête d'autorisation avec un jeton bearer