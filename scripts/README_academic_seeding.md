# Scripts de Seeding pour les Données Académiques

Ce dossier contient les scripts pour populer la base de données avec les données académiques de base (domaines, niveaux et mentions d'étude) basées sur les habilitations réelles d'établissements malgaches.

## Scripts disponibles

### 1. `seed_domains.py`

Popule la table des domaines d'étude avec 6 domaines principaux basés sur les habilitations réelles :

- Sciences de la Société
- Sciences et Technologies
- Sciences de la Santé
- Sciences de l'Ingénieur
- Sciences de l'Education
- Arts, Lettres et Sciences Humaines

### 2. `seed_levels.py`

Popule la table des niveaux d'étude avec 6 niveaux académiques basés sur les habilitations réelles :

- Licence (L)
- Master (M)
- Diplôme de Technicien Supérieur (DTS)
- Diplôme de Technicien Supérieur Spécialisé (DTSS)
- Doctorat (PhD)
- Diplôme d'Ingénieur (DI)

### 3. `seed_mentions.py`

Popule la table des mentions d'étude organisées par domaine basées sur les habilitations réelles.
**Attention :** Ce script nécessite que les domaines soient déjà créés.

### 4. `seed_all_academic.py` (Recommandé)

Script principal qui exécute tous les scripts de seeding dans le bon ordre.

## Utilisation

### Méthode recommandée - Script complet

```bash
# Exécuter tous les scripts de seeding
python scripts/seed_all_academic.py

# Afficher uniquement les statistiques
python scripts/seed_all_academic.py --stats-only
```

### Méthode manuelle - Scripts individuels

```bash
# 1. D'abord les domaines
python scripts/seed_domains.py

# 2. Ensuite les niveaux (indépendant)
python scripts/seed_levels.py

# 3. Enfin les mentions (dépend des domaines)
python scripts/seed_mentions.py
```

## Ordre d'exécution important

1. **Domaines** doivent être créés en premier
2. **Niveaux** peuvent être créés indépendamment
3. **Mentions** doivent être créées après les domaines (dépendance)

## Fonctionnalités

- ✅ **Détection des doublons** : Les scripts vérifient si les données existent déjà
- 🔄 **Exécution multiple** : Peut être exécuté plusieurs fois sans créer de doublons
- 📊 **Statistiques** : Affiche le nombre d'éléments créés/existants
- 🎯 **Messages informatifs** : Indique clairement le statut de chaque opération

## Structure des données

### Domaines (15 domaines)

Chaque domaine contient :

- `name` : Nom du domaine
- `created_at` / `updated_at` : Horodatage automatique

### Niveaux (21 niveaux)

Chaque niveau contient :

- `name` : Nom complet du niveau
- `acronym` : Acronyme du niveau (ex: "BAC", "L", "M", "PhD")
- `created_at` / `updated_at` : Horodatage automatique

### Mentions (104 mentions)

Chaque mention contient :

- `name` : Nom de la mention
- `domain` : Référence vers le domaine parent
- `created_at` / `updated_at` : Horodatage automatique

## Exemples de données

### Domaines

- Sciences et Technologies
- Sciences Humaines et Sociales
- Sciences Economiques et de Gestion

### Niveaux

- Baccalauréat (BAC)
- Licence (L)
- Master (M)
- Doctorat (PhD)

### Mentions par domaine

**Sciences et Technologies :**

- Informatique
- Mathématiques
- Physique
- Chimie
- Biologie

**Sciences Economiques et de Gestion :**

- Économie
- Gestion
- Finance
- Comptabilité
- Marketing

## Dépendances

- Tortoise ORM configuré
- Base de données accessible
- Modèles Domain, Level, Mention disponibles

## Gestion des erreurs

- Connexion à la base de données vérifiée
- Gestion des domaines manquants pour les mentions
- Messages d'erreur explicites
- Fermeture propre des connexions

## Logs et monitoring

Les scripts affichent :

- 🌱 Démarrage du seeding
- ✅ Éléments existants détectés
- ✨ Nouveaux éléments créés
- 📊 Statistiques finales
- ⚠️ Avertissements (domaines manquants, etc.)
- ❌ Erreurs avec détails
