import logging
from typing import Optional

from django.core.paginator import Paginator
from django.db import IntegrityError

from apps.establishment.models import Establishment
from apps.establishment_type.models import EstablishmentType
from apps.sector.models import Sector  # Ajout de l'import pour Sector
from apps.users.models import User
from core.domain.entities.establishment_entity import EstablishmentEntity
from core.domain.entities.pagination import PaginatedResult
from core.interfaces.establishment_repository import IEstablishmentRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository
from infrastructure.db.django_model_to_entity import (
    EstablishmentToEntityMetadata,
    establishment_to_entity,
)
from presentation.exceptions import (
    ConflictError,
    DatabaseError,
    NotFoundError,
    UnprocessableEntityError,
)

logger = logging.getLogger(__name__)


class DjangoEstablishmentRepository(
    DjangoBaseRepository[EstablishmentEntity, Establishment, int],
    IEstablishmentRepository,
):
    """Django implementation of the repository for establishments"""

    def __init__(self):
        super().__init__(Establishment, EstablishmentEntity)

    def _to_entity(self, db_obj: Establishment) -> EstablishmentEntity:
        """Converts a Django Establishment model to an EstablishmentEntity."""
        return establishment_to_entity(
            db_obj,
            metadata=EstablishmentToEntityMetadata(
                establishment_type=True,
                sector=True,
                formations=True,
            ),
        )

    def get_by_name(self, name: str) -> Optional[EstablishmentEntity]:
        """Retrieves an establishment by its name"""
        try:
            establishment = self.model.objects.get(name=name)
            return self._to_entity(establishment)
        except self.model.DoesNotExist:
            return None

    def check_establishment_type_exists(self, establishment_type_id: int) -> bool:
        """Checks if the establishment type with the given ID exists"""
        return EstablishmentType.objects.filter(id=establishment_type_id).exists()

    def check_sector_exists(self, sector_id: int) -> bool:
        """Checks if the sector with the given ID exists"""
        return Sector.objects.filter(id=sector_id).exists()

    def create(self, obj: EstablishmentEntity) -> EstablishmentEntity:
        """Creates a new establishment"""
        if not self.check_establishment_type_exists(obj.establishment_type_id):
            raise UnprocessableEntityError()

        # Vérifier que le secteur existe
        if not self.check_sector_exists(obj.sector_id):
            raise UnprocessableEntityError()

        created_by_id = obj.created_by
        updated_by_id = obj.updated_by

        obj_dict = obj.model_dump(
            exclude={
                "id",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
                "establishment_type_id",
                "establishment_type",
                "sector_id",
                "sector",
                "rating",
                "formations",
            }
        )

        db_obj = self.model(**obj_dict)

        # Set the establishment_type
        db_obj.establishment_type = EstablishmentType.objects.get(
            id=obj.establishment_type_id
        )

        # Set the sector
        db_obj.sector = Sector.objects.get(id=obj.sector_id)

        # Set tracking fields
        if created_by_id:
            db_obj.created_by = User.objects.get(id=created_by_id)

        if updated_by_id:
            db_obj.updated_by = User.objects.get(id=updated_by_id)

        db_obj.save()
        return self._to_entity(db_obj)

    def update(self, id: int, obj: EstablishmentEntity) -> EstablishmentEntity:
        """
        Met à jour un établissement existant en gérant correctement les relations.
        """
        try:
            updated_by_id = obj.updated_by

            db_obj = self.model.objects.get(id=id)

            # Mettre à jour les propriétés simples (non relationnelles)
            obj_dict = obj.model_dump(
                exclude={
                    "id",
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                    "establishment_type",
                    "establishment_type_id",
                    "sector",
                    "sector_id",
                    "formations",
                }
            )

            for key, value in obj_dict.items():
                setattr(db_obj, key, value)

            # Gérer les relations manuellement si leurs IDs sont présents
            if obj.establishment_type_id:
                db_obj.establishment_type = EstablishmentType.objects.get(
                    id=obj.establishment_type_id
                )

            if obj.sector_id:
                db_obj.sector = Sector.objects.get(id=obj.sector_id)

            # Mettre à jour l'utilisateur qui a fait la modification
            if updated_by_id:
                db_obj.updated_by = User.objects.get(id=updated_by_id)

            db_obj.save()
            return self._to_entity(db_obj)

        except self.model.DoesNotExist:
            logger.warning(f"{self.model.__name__} with id {id} not found for update.")
            raise NotFoundError()
        except IntegrityError as e:
            logger.error(
                f"Database integrity error updating {self.model.__name__} with id {id}: {e}",
                exc_info=True,
            )
            raise ConflictError()
        except Exception as e:
            logger.error(
                f"Database error updating {self.model.__name__} with id {id}: {e}",
                exc_info=True,
            )
            raise DatabaseError()

    def _paginate_queryset(self, queryset, pagination_params=None):
        """Pagine un queryset Django et retourne un objet PaginatedResult."""
        # Valeurs par défaut de pagination
        page = 1
        per_page = 10

        if pagination_params:
            page = pagination_params.page
            per_page = pagination_params.per_page

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return PaginatedResult(
            items=list(page_obj),
            total_items=paginator.count,
            page=page,
            per_page=per_page,
            total_pages=paginator.num_pages,
        )

    def filter_establishments(
        self,
        name: Optional[str] = None,
        acronyme: Optional[str] = None,
        establishment_type_id: Optional[int] = None,
        city_id: Optional[int] = None,
        region_id: Optional[int] = None,
        domain_id: Optional[int] = None,
        level_id: Optional[int] = None,
        pagination_params=None,
    ) -> PaginatedResult[EstablishmentEntity]:
        """
        Filtre les établissements selon divers critères.

        Args:
            name: Filtre par nom (commence par)
            acronyme: Filtre par acronyme (commence par)
            establishment_type_id: Filtre par type d'établissement
            city_id: Filtre par ville du secteur
            region_id: Filtre par région de la ville du secteur
            domain_id: Filtre par domaine de formation proposé
            level_id: Filtre par niveau de formation proposé
            pagination_params: Paramètres de pagination

        Returns:
            Un résultat paginé d'établissements filtrés
        """
        query = self.model.objects.all()

        # Application des filtres existants
        if name:
            query = query.filter(name__istartswith=name)

        if acronyme:
            query = query.filter(acronyme__istartswith=acronyme)

        if establishment_type_id:
            query = query.filter(establishment_type_id=establishment_type_id)

        if city_id:
            query = query.filter(sector__city_id=city_id)

        if region_id:
            query = query.filter(sector__city__region_id=region_id)

        # Correction du filtre par domaine - Nous devons suivre la relation jusqu'à mention.domain
        if domain_id:
            query = query.filter(formation__mention__domain_id=domain_id).distinct()

        # Filtre par niveau
        if level_id:
            query = query.filter(formation__level_id=level_id).distinct()

        # Gestion de la pagination
        paginated_result = self._paginate_queryset(query, pagination_params)

        # Convertir les résultats en entités
        items = [self._to_entity(item) for item in paginated_result.items]

        return PaginatedResult(
            items=items,
            total_items=paginated_result.total_items,
            page=paginated_result.page,
            per_page=paginated_result.per_page,
            total_pages=paginated_result.total_pages,
        )
