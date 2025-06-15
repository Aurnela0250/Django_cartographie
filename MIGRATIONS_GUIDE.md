# Guide des Migrations SQLModel avec Alembic

## 📋 Aperçu

Ce projet utilise **Alembic** pour gérer les migrations de base de données SQLModel. Alembic est l'outil recommandé pour les changements de schéma avec SQLAlchemy/SQLModel.

## 🏗️ Architecture

```
📁 projet/
├── 📁 alembic/                     # Configuration Alembic
│   ├── 📄 env.py                   # Configuration environnement
│   ├── 📄 script.py.mako          # Template migrations
│   └── 📁 versions/               # Fichiers de migration
├── 📄 alembic.ini                 # Configuration Alembic
├── 📁 infrastructure/db/fastapi/
│   ├── 📄 engine.py               # Moteur SQLModel async
│   └── 📁 models/                 # Modèles SQLModel
└── 📄 .env                        # Variables d'environnement
```

## 🚀 Configuration Initiale Terminée

✅ **Alembic est configuré et prêt !**

- Base de données : PostgreSQL (`postgres_cartographie`)
- Modèle User avec champs d'audit complets
- Migration automatique fonctionnelle
- Support asyncpg pour PostgreSQL async

## 📝 Commandes Principales

### Créer une nouvelle migration

```bash
# Migration automatique (recommandé)
alembic revision --autogenerate -m "Description du changement"

# Migration manuelle vide
alembic revision -m "Description du changement"
```

### Appliquer les migrations

```bash
# Appliquer toutes les migrations en attente
alembic upgrade head

# Appliquer une migration spécifique
alembic upgrade <revision_id>

# Avancer d'une migration
alembic upgrade +1
```

### Voir l'état actuel

```bash
# Voir la révision actuelle
alembic current

# Voir l'historique des migrations
alembic history

# Voir les migrations en attente
alembic history --rev-range current:head
```

### Revenir en arrière

```bash
# Revenir d'une migration
alembic downgrade -1

# Revenir à une révision spécifique
alembic downgrade <revision_id>

# Revenir à la base (attention !)
alembic downgrade base
```

## 🔧 Workflow de Développement

### 1. Modifier un modèle SQLModel

```python
# infrastructure/db/fastapi/models/user_model.py
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    # ✨ Nouveau champ
    phone: Optional[str] = Field(default=None)
```

### 2. Générer une migration

```bash
alembic revision --autogenerate -m "Add phone field to user"
```

### 3. Vérifier la migration générée

```python
# alembic/versions/xxxxx_add_phone_field_to_user.py
def upgrade() -> None:
    op.add_column('user', sa.Column('phone', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('user', 'phone')
```

### 4. Appliquer la migration

```bash
alembic upgrade head
```

### 5. Vérifier en base

```bash
docker exec postgres_cartographie psql -U cartographie -d cartographie_db -c "\d user"
```

## ⚠️ Bonnes Pratiques

### ✅ À Faire

- **Toujours vérifier** les migrations générées avant de les appliquer
- **Tester les migrations** en local avant la production
- **Faire des sauvegardes** avant les migrations importantes
- **Utiliser des descriptions claires** pour les migrations
- **Revérifier la logique** des fonctions `upgrade()` et `downgrade()`

### ❌ À Éviter

- **Ne jamais modifier** une migration déjà appliquée en production
- **Ne pas supprimer** les fichiers de migration sans raison
- **Éviter les migrations destructives** sans sauvegarde
- **Ne pas oublier** les valeurs par défaut pour les colonnes NOT NULL

## 🛠️ Types de Migrations Courants

### Ajouter une colonne

```python
def upgrade():
    op.add_column('user', sa.Column('new_field', sa.String(), nullable=True))

def downgrade():
    op.drop_column('user', 'new_field')
```

### Modifier une colonne

```python
def upgrade():
    op.alter_column('user', 'email',
                   existing_type=sa.String(100),
                   type_=sa.String(255))

def downgrade():
    op.alter_column('user', 'email',
                   existing_type=sa.String(255),
                   type_=sa.String(100))
```

### Ajouter un index

```python
def upgrade():
    op.create_index('ix_user_phone', 'user', ['phone'])

def downgrade():
    op.drop_index('ix_user_phone', 'user')
```

### Ajouter une clé étrangère

```python
def upgrade():
    op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_user_role', 'user', 'role', ['role_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_user_role', 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')
```

## 🐛 Résolution de Problèmes

### Migration échoue avec contrainte de clé étrangère

```bash
# Vérifier les dépendances
docker exec postgres_cartographie psql -U cartographie -d cartographie_db -c "
SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='user';
"
```

### Réinitialiser Alembic (attention !)

```bash
# Supprimer la table de version (perte de l'historique)
docker exec postgres_cartographie psql -U cartographie -d cartographie_db -c "DROP TABLE alembic_version;"

# Stamper à la révision actuelle
alembic stamp head
```

### Conflits de révision

```bash
# Voir les branches
alembic branches

# Merger les branches
alembic merge -m "Merge revisions" rev1 rev2
```

## 📊 État Actuel du Projet

**Base de données :** `cartographie_db`  
**Révision actuelle :** `05d651660155`  
**Dernière migration :** "Add full_name field to user table"

**Modèles configurés :**

- ✅ `User` - Complet avec champs d'audit

**Champs User :**

- `id` (PK, auto-increment)
- `email` (unique, indexed)
- `password`
- `active` (défaut: true)
- `is_superuser` (défaut: false)
- `full_name` (optionnel)
- `created_at` (auto-timestamp)
- `updated_at` (auto-timestamp)
- `created_by` (FK vers user, optionnel)
- `updated_by` (FK vers user, optionnel)

## 🚀 Prochaines Étapes

1. **Ajouter plus de modèles** SQLModel selon les besoins
2. **Configurer des endpoints** FastAPI pour CRUD
3. **Implémenter l'authentification** avec les champs user
4. **Ajouter des seeds/fixtures** pour les données de test
5. **Configurer les tests** avec base de données de test

## 📞 Support

Pour toute question sur les migrations :

1. Vérifier ce guide
2. Consulter la [documentation Alembic](https://alembic.sqlalchemy.org/)
3. Vérifier les logs avec `alembic history -v`

---

**⚡ Migration System Ready!** Le système de migration est configuré et prêt pour l'évolution de votre schéma de base de données.
