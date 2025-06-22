# Contexte Technique : OrientationMada

## Technologies Utilisées

- **Langage de programmation** : Python 3
- **Framework Web** : Django avec Django Ninja
- **ORM** : Tortoise ORM (utilisé à la place de l'ORM Django par défaut)
- **Base de données** :
  - PostgreSQL (principal)
  - SQLite (pour les tests)
- **Cache** : Redis
- **Authentification** : JWT (JSON Web Tokens)
- **Autorisation** : OpenFGA
- **Conteneurisation** : Docker
- **Gestion des dépendances** : uv
- **Automatisation** : Makefile

## Configuration du Développement

- Les dépendances sont gérées via `uv` et `pyproject.toml`.
- Des scripts `Makefile` sont disponibles pour automatiser les tâches courantes.
- L'environnement de développement est défini dans `.env.development`.

## Contraintes Techniques

- L'API doit être performante et capable de gérer un grand volume de requêtes.
- La sécurité est primordiale, notamment pour la gestion des utilisateurs et des tokens d'authentification.
