import logging

from tortoise.transactions import atomic

from core.entities.filters import FormationFilters
from core.entities.formation_entity import FormationEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.formation_repository import IFormationRepository
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class FormationUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les formations"""

    def __init__(
        self,
        formation_repository: IFormationRepository,
    ):
        self.formation_repository = formation_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(
        self,
        formation_data: FormationEntity,
    ) -> FormationEntity:
        try:
            existing_formation = await self.formation_repository.get_by_name(
                formation_data.name
            )
            if existing_formation:
                self.logger.warning(
                    f"Formation with name '{formation_data.name}' already exists"
                )
                raise ConflictException()
            created_formation = await self.formation_repository.create(formation_data)
            return created_formation
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during formation creation: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, formation_id: int) -> FormationEntity:
        try:
            formation = await self.formation_repository.get(formation_id)
            if not formation:
                raise NotFoundException()
            return formation
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during formation retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self,
        formation_id: int,
        formation_data: FormationEntity,
    ) -> FormationEntity:
        try:
            existing_formation = await self.formation_repository.get(formation_id)
            if not existing_formation:
                raise NotFoundException()
            if formation_data.name != existing_formation.name:
                name_exists = await self.formation_repository.get_by_name(
                    formation_data.name
                )
                if name_exists and name_exists.id != formation_id:
                    self.logger.warning(
                        f"Cannot update: Formation with name '{formation_data.name}' already exists"
                    )
                    raise ConflictException()
            updated_formation = await self.formation_repository.update(
                formation_id, formation_data
            )
            return updated_formation
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during formation update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, formation_id: int) -> bool:
        try:
            existing_formation = await self.formation_repository.get(formation_id)
            if not existing_formation:
                raise NotFoundException()
            result = await self.formation_repository.delete(formation_id)
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during formation deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[FormationEntity]:
        try:
            formations = await self.formation_repository.get_all(
                pagination_params=pagination_params
            )
            return formations
        except Exception as e:
            self.logger.error(f"Unexpected error during formations retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: FormationFilters,
    ) -> PaginatedResult[FormationEntity]:
        try:
            formations = await self.formation_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return formations
        except Exception as e:
            self.logger.error(f"Unexpected error during formations filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
