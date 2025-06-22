# Cartographie API FastAPI

API pour le projet de cartographie des établissements, formations et situation des anciens étudiants.

## Installation

1.  **Cloner le projet**

    ```bash
    git clone <URL_DU_PROJET>
    cd Django_cartographie
    ```

2.  **Installer les dépendances**

    Ce projet utilise `uv` pour la gestion des dépendances. Pour installer les dépendances, exécutez :

    ```bash
    make install
    ```

## Commandes disponibles

Le `Makefile` contient plusieurs commandes pour faciliter le développement.

### Serveur

- **Lancer le serveur de développement :**
  ```bash
  make run
  ```
- **Lancer le serveur de production :**
  ```bash
  make start
  ```

### Tests

- **Lancer tous les tests :**
  ```bash
  make test-all
  ```
- **Lancer les tests unitaires :**
  ```bash
  make test-unit
  ```
- **Lancer les tests pour un module spécifique (par ex. `city`) :**
  ```bash
  make test-unit-city
  ```
- **Lancer les tests pour le module `domain` :**
  ```bash
  make test-unit-domain
  ```
- **Lancer un test spécifique (par ex. `create` pour `domain`) :**
  ```bash
  make test-unit-domain-create
  ```
- **Lancer les tests pour le module `establishment_type` :**
  ```bash
  make test-unit-establishment-type
  ```

### Linting et Formatage

- **Vérifier le code (linting) :**
  ```bash
  make lint
  ```
- **Formater le code :**
  ```bash
  make format
  ```

Pour voir toutes les commandes disponibles, exécutez :

```bash
make help
```
