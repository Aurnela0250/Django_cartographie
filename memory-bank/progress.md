# Progression : OrientationMada

## Ce qui fonctionne

D'après l'analyse du code existant, les fonctionnalités suivantes semblent être implémentées, au moins partiellement :

- **Architecture de base** : Le projet est structuré en couches (core, infrastructure, presentation) suivant les principes de l'architecture propre.
- **Configuration du projet** : La configuration Django est en place, incluant la base de données (PostgreSQL), le cache (Redis), et l'authentification (JWT).
- **Modèles de données** : Les modèles Tortoise ORM pour les entités principales (User, Region, City, Establishment, Formation, etc.) sont définis.
- **Authentification des utilisateurs** : Un système d'authentification basé sur JWT est configuré.
- **Gestion des erreurs** : Un système d'exceptions personnalisées est en place pour gérer les erreurs de l'API.
- **Tests** : Une configuration de base pour les tests unitaires et e2e avec pytest est présente, utilisant une base de données en mémoire.
- **API de base** : Des routes API (endpoints) sont probablement définies dans la couche `presentation` pour exposer les fonctionnalités.

## Ce qui reste à construire

- **Fonctionnalités de recherche avancée** : Vérifier si la recherche avec filtres est complète et optimisée.
- **Moteur de recommandations** : L'implémentation du moteur de recommandations basé sur les statistiques et les profils est probablement à développer ou à finaliser.
- **Chatbot IA** : Le chatbot intelligent est une fonctionnalité majeure qui nécessite une implémentation complète.
- **Couverture de tests** : La couverture de tests doit être étendue pour garantir la fiabilité du code.
- **Documentation de l'API** : La documentation des endpoints de l'API (par exemple avec Swagger/OpenAPI) doit être complète.
- **Déploiement** : Les configurations pour le déploiement en production (par exemple avec Docker Compose) doivent être finalisées et testées.

## Statut Actuel

Le projet est bien avancé sur le plan de l'infrastructure et de l'architecture de base. Plusieurs fonctionnalités clés sont déjà en place. Le focus doit maintenant se porter sur le développement des fonctionnalités à plus haute valeur ajoutée (recommandations, chatbot) et sur la consolidation de l'existant (tests, documentation).

## Problèmes Connus

- Aucun identifié pour le moment, mais une analyse plus approfondie du code est nécessaire.

## Évolution des Décisions

- Le projet utilise Django avec Django Ninja, et non FastAPI comme supposé initialement.
- Tortoise ORM est utilisé à la place de l'ORM Django, ce qui est un choix de conception important.
- OpenFGA est utilisé pour la gestion des autorisations, ce qui indique un besoin de contrôle d'accès fin.
