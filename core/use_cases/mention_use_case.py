import logging

from tortoise.transactions import atomic

from core.entities.filters import MentionFilters
from core.entities.mention import MentionEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.mention_repository import IMentionRepository
from presentation.exceptions import (
    ConflictException,
    DatabaseDoesNotExistException,
    DatabaseIntegrityException,
    InternalServerErrorException,
    NotFoundException,
)


class MentionUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les mentions"""

    def __init__(
        self,
        mention_repository: IMentionRepository,
    ):
        self.mention_repository = mention_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(
        self,
        mention_data: MentionEntity,
    ) -> MentionEntity:
        try:
            return await self.mention_repository.create(mention_data)
        except DatabaseIntegrityException as e:
            self.logger.warning(f"Conflict creating mention '{mention_data.name}': {e}")
            raise ConflictException(str(e))
        except Exception as e:
            self.logger.error(f"Failed to create mention: {e}")
            raise InternalServerErrorException(str(e))

    @atomic()
    async def get(self, mention_id: int) -> MentionEntity:
        try:
            return await self.mention_repository.get(mention_id)
        except DatabaseDoesNotExistException as e:
            self.logger.warning(f"Mention with id {mention_id} not found: {e}")
            raise NotFoundException(str(e))
        except Exception as e:
            self.logger.error(f"Failed to get mention {mention_id}: {e}")
            raise InternalServerErrorException(str(e))

    @atomic()
    async def update(
        self,
        mention_id: int,
        mention_data: dict,
    ) -> MentionEntity:
        try:
            mention_entity = MentionEntity(**mention_data)
            return await self.mention_repository.update(mention_id, mention_entity)
        except DatabaseDoesNotExistException as e:
            self.logger.warning(
                f"Mention with id {mention_id} not found on update: {e}"
            )
            raise NotFoundException(str(e))
        except DatabaseIntegrityException as e:
            self.logger.warning(f"Conflict updating mention {mention_id}: {e}")
            raise ConflictException(str(e))
        except Exception as e:
            self.logger.error(f"Failed to update mention {mention_id}: {e}")
            raise InternalServerErrorException(str(e))

    @atomic()
    async def delete(self, mention_id: int) -> bool:
        try:
            return await self.mention_repository.delete(mention_id)
        except DatabaseDoesNotExistException as e:
            self.logger.warning(
                f"Mention with id {mention_id} not found on delete: {e}"
            )
            raise NotFoundException(str(e))
        except Exception as e:
            self.logger.error(f"Failed to delete mention {mention_id}: {e}")
            raise InternalServerErrorException(str(e))

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[MentionEntity]:
        try:
            mentions = await self.mention_repository.get_all(
                pagination_params=pagination_params
            )
            return mentions
        except Exception as e:
            self.logger.error(f"Unexpected error during mentions retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: MentionFilters,
    ) -> PaginatedResult[MentionEntity]:
        try:
            mentions = await self.mention_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return mentions
        except Exception as e:
            self.logger.error(f"Unexpected error during mentions filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
