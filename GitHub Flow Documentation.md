# Guide GitHub Flow pour notre projet Django

## Introduction

Ce document décrit notre stratégie de branches Git basée sur GitHub Flow, une approche légère et efficace adaptée à notre projet Django. GitHub Flow permet un développement continu avec des déploiements fréquents, tout en maintenant un code stable et de qualité.

## Structure des branches

GitHub Flow utilise une structure minimaliste avec seulement deux types de branches:

1. **`main`** - La branche principale

   - Toujours déployable en production
   - Contient le code stable et validé
   - Protégée contre les commits directs

2. **Branches de fonctionnalités** - Créées à partir de `main`
   - Nommées de façon descriptive (ex: `feature/auth-system`, `fix/login-error`)
   - Courte durée de vie
   - Une branche = une fonctionnalité ou correction

## Conventions de nommage des branches

Pour maintenir une organisation claire, nous utiliserons les préfixes suivants pour nos branches:

- `feature/` - Pour les nouvelles fonctionnalités

  - Exemple: `feature/user-authentication`
  - Exemple: `feature/payment-integration`

- `fix/` - Pour les corrections de bugs

  - Exemple: `fix/login-error`
  - Exemple: `fix/api-response-format`

- `refactor/` - Pour les refactorisations de code

  - Exemple: `refactor/clean-architecture-implementation`
  - Exemple: `refactor/performance-optimization`

- `docs/` - Pour les mises à jour de documentation
  - Exemple: `docs/api-documentation`
  - Exemple: `docs/setup-instructions`

## Workflow GitHub Flow

### 1. Création d'une branche

Toujours partir de la branche `main` à jour:

```bash
git checkout main
git pull
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### 2. Développement

Travaillez sur votre branche en effectuant des commits réguliers:

```bash
# Après avoir fait des modifications
git add .
git commit -m "Description claire des modifications"
```

Conseils pour les messages de commit:

- Utilisez l'impératif présent: "Add feature" au lieu de "Added feature"
- Soyez précis mais concis (< 50 caractères)
- Si nécessaire, ajoutez des détails après une ligne vide

### 3. Synchronisation régulière

Poussez régulièrement votre branche vers le dépôt distant:

```bash
git push -u origin feature/ma-nouvelle-fonctionnalite
```

Si `main` a évolué, synchronisez votre branche:

```bash
git checkout main
git pull
git checkout feature/ma-nouvelle-fonctionnalite
git merge main
# Résolvez les conflits si nécessaire
```

### 4. Pull Request (PR)

Lorsque votre fonctionnalité est prête:

1. Créez une Pull Request sur GitHub
2. Ajoutez une description détaillée
3. Associez la PR aux issues concernées
4. Demandez une revue à au moins un membre de l'équipe

### 5. Revue de code

Le processus de revue comprend:

- Vérification du respect des normes de code
- Tests fonctionnels
- Validation des exigences

### 6. Déploiement en test

Notre workflow GitHub Actions déploie automatiquement en environnement de test lors de la création d'une PR pour valider les changements.

### 7. Fusion

Une fois approuvée et testée, la PR peut être fusionnée dans `main`:

- Utilisez "Squash and merge" pour garder l'historique propre
- Assurez-vous que le message de commit résume bien les changements

### 8. Déploiement en production

Après fusion dans `main`, notre workflow GitHub Actions déploie automatiquement en production.

### 9. Suppression de la branche

Une fois fusionnée, supprimez la branche de fonctionnalité:

```bash
git checkout main
git pull
git branch -d feature/ma-nouvelle-fonctionnalite
git push origin --delete feature/ma-nouvelle-fonctionnalite
```

## Gestion des environnements

Nous utilisons GitHub Environments pour gérer nos différents environnements:

1. **Environnement de test**

   - Déploiement automatique lors de la création d'une PR
   - URL: `https://test.notre-projet.com`

2. **Environnement de production**
   - Déploiement automatique après fusion dans `main`
   - URL: `https://notre-projet.com`

## Situation d'urgence (hotfix)

En cas de bug critique en production:

1. Créez une branche `fix/` à partir de `main`
2. Développez et testez le correctif
3. Créez une PR avec l'étiquette "Urgent"
4. Après revue accélérée, fusionnez dans `main`

## FAQ

### Comment gérer une fonctionnalité complexe qui prendra plusieurs semaines?

Divisez-la en sous-fonctionnalités plus petites qui peuvent être développées et fusionnées séparément.

### Comment annuler un changement déjà fusionné?

Créez une nouvelle branche `fix/` qui annule le changement problématique et suivez le processus normal.

### Dois-je mettre à jour ma branche de fonctionnalité si `main` a changé?

Oui, il est recommandé de synchroniser régulièrement votre branche avec `main` pour éviter des conflits majeurs lors de la fusion.

---

Document créé le: 23/03/2025  
Dernière mise à jour: 23/03/2025

---
