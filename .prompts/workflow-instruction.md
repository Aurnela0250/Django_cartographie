# Workflow pour les fonctionnalité

1. crée l'entity et ajouter les attribut de la class dans `core/domain/entities/`
2. crée l'interface du repository dans `core/interfaces/`
3. Implementer l'interface du repository dans `infrastructure/db/`
4. créer les schemas pour le controller dans `presentation/schema/`
5. Implementer le use case dans `core/use_case/`
6. implementer le controller dans `presentation/api/v1/endpoints/`
