# Workflow pour les fonctionnalité

1. crée l'entity et ajouter les attribut de la class dans `core/domain/entities/`
2. crée l'interface du repository dans `core/interfaces/`
3. Ajouter la fontion `*_to_entity` dans `infrastructure/db/django_model_to_entity.py`
4. Implementer l'interface du repository dans `infrastructure/db/`
5. créer les schemas pour le controller dans `presentation/schema/`
6. Implementer le use case dans `core/use_case/`
7. implementer le controller dans `presentation/api/v1/endpoints/`
8. Ajouter le controller dans la list des controller `presentation/api/v1/router.py`
