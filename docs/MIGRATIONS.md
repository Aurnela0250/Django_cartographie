# Migrations SQLModel avec Alembic

Ce projet utilise **Alembic** pour gérer les migrations de base de données avec **SQLModel** et **PostgreSQL**.

## Configuration

### Variables d'environnement requises

Créez un fichier `.env` à la racine du projet avec :

```bash
# Configuration de la base de données
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=cartographie
DB_ECHO=false  # true pour voir les requêtes SQL
```

### Structure des fichiers

```
├── alembic/                    # Répertoire Alembic
│   ├── env.py                 # Configuration d'environnement (modifié pour SQLModel + asyncpg)
│   ├── script.py.mako         # Template pour les migrations
│   └── versions/              # Scripts de migration
├── alembic.ini                # Configuration Alembic
├── infrastructure/db/fastapi/
│   ├── engine.py              # Moteur SQLAlchemy asynchrone
│   ├── models/                # Modèles SQLModel
│   │   ├── __init__.py        # Import des modèles
│   │   └── user_model.py      # Modèle User
└── scripts/
    ├── setup_migrations.py    # Script d'initialisation automatique
    └── test_alembic_config.py # Script de test de configuration
```

## Utilisation

### Initialisation (première fois)

1. **Test de la configuration :**

   ```bash
   python scripts/test_alembic_config.py
   ```

2. **Initialisation automatique :**

   ```bash
   python scripts/setup_migrations.py
   ```

3. **Ou initialisation manuelle :**

   ```bash
   # Créer la première migration
   alembic revision --autogenerate -m "Initial migration"

   # Appliquer les migrations
   alembic upgrade head
   ```

### Commandes courantes

```bash
# Créer une nouvelle migration après modification des modèles
alembic revision --autogenerate -m "Description des changements"

# Appliquer toutes les migrations pendantes
alembic upgrade head

# Voir l'état actuel
alembic current

# Voir l'historique des migrations
alembic history

# Revenir à une migration précédente
alembic downgrade <revision_id>

# Voir les migrations pendantes
alembic show head
```

### Workflow de développement

1. **Modifier un modèle SQLModel :**

   ```python
   # Dans infrastructure/db/fastapi/models/user_model.py
   class User(SQLModel, table=True):
       id: Optional[int] = Field(default=None, primary_key=True)
       email: str = Field(unique=True, index=True)
       # Ajouter nouveau champ :
       full_name: Optional[str] = Field(default=None)
   ```

2. **Générer la migration automatiquement :**

   ```bash
   alembic revision --autogenerate -m "Add full_name to User"
   ```

3. **Vérifier le script généré :**

   - Ouvrir le fichier dans `alembic/versions/`
   - Vérifier que les changements sont corrects
   - Modifier si nécessaire

4. **Appliquer la migration :**
   ```bash
   alembic upgrade head
   ```

## Fonctionnalités avancées

### Migrations de données

Pour inclure des modifications de données :

```python
# Dans le script de migration
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

def upgrade():
    # Migration de schéma
    op.add_column('user', sa.Column('full_name', sa.String(), nullable=True))

    # Migration de données
    user_table = table('user',
        column('id', sa.Integer),
        column('email', sa.String),
        column('full_name', sa.String)
    )

    # Exemple : remplir full_name basé sur email
    op.execute(
        user_table.update().values(
            full_name=func.split_part(user_table.c.email, '@', 1)
        )
    )
```

### Gestion des environnements

Pour différents environnements, modifiez les variables d'environnement :

```bash
# Développement
DB_NAME=cartographie_dev

# Test
DB_NAME=cartographie_test

# Production
DB_NAME=cartographie_prod
```

## Résolution de problèmes

### Erreur : "Target database is not up to date"

```bash
# Vérifier l'état actuel
alembic current

# Forcer la synchronisation (attention : peut perdre des données)
alembic stamp head
```

### Erreur : "Can't locate revision identified by"

```bash
# Voir l'historique
alembic history

# Repartir de zéro (développement uniquement)
alembic stamp base
alembic upgrade head
```

### Conflit de migration

1. Identifier les branches :

   ```bash
   alembic branches
   ```

2. Fusionner les branches :
   ```bash
   alembic merge -m "Merge branches" <rev1> <rev2>
   ```

## Bonnes pratiques

1. **Toujours vérifier les migrations générées** avant de les appliquer
2. **Tester les migrations** sur une copie de la base de données de production
3. **Garder les migrations petites** et atomiques
4. **Documenter les migrations complexes** avec des commentaires
5. **Sauvegarder** avant d'appliquer des migrations importantes
6. **Ne jamais modifier** une migration déjà appliquée en production

## Intégration avec le code applicatif

### Démarrage de l'application

```python
# Dans main.py
from infrastructure.db.fastapi.engine import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # En développement uniquement - utiliser Alembic en production
    if os.getenv("ENVIRONMENT") == "development":
        await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
```

### Tests

```python
# Utiliser une base de données de test séparée
import pytest
from alembic import command
from alembic.config import Config

@pytest.fixture
async def db_with_migrations():
    # Appliquer les migrations pour les tests
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield

    # Nettoyer après les tests
    command.downgrade(alembic_cfg, "base")
```

## Références

- [Documentation Alembic](https://alembic.sqlalchemy.org/)
- [Documentation SQLModel](https://sqlmodel.tiangolo.com/)
- [Guide Alembic + SQLModel](https://github.com/tiangolo/sqlmodel/issues/61)
