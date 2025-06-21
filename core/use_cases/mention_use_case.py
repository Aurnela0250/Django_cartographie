import logging

from tortoise.transactions import atomic

from core.entities.filters import MentionFilters
from core.entities.mention import MentionEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.mention_repository import IMentionRepository
from presentation.exceptions import (
    ConflictException,
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
            existing_mention = await self.mention_repository.get_by_name(
                mention_data.name
            )
            if existing_mention:
                self.logger.warning(
                    f"Mention with name '{mention_data.name}' already exists"
                )
                raise ConflictException()
            created_mention = await self.mention_repository.create(mention_data)
            return created_mention
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during mention creation: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, mention_id: int) -> MentionEntity:
        try:
            mention = await self.mention_repository.get(mention_id)
            if not mention:
                raise NotFoundException()
            return mention
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during mention retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self,
        mention_id: int,
        mention_data: MentionEntity,
    ) -> MentionEntity:
        try:
            existing_mention = await self.mention_repository.get(mention_id)
            if not existing_mention:
                raise NotFoundException()
            if mention_data.name != existing_mention.name:
                name_exists = await self.mention_repository.get_by_name(
                    mention_data.name
                )
                if name_exists and name_exists.id != mention_id:
                    self.logger.warning(
                        f"Cannot update: Mention with name '{mention_data.name}' already exists"
                    )
                    raise ConflictException()
            updated_mention = await self.mention_repository.update(
                mention_id, mention_data
            )
            return updated_mention
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during mention update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, mention_id: int) -> bool:
        try:
            existing_mention = await self.mention_repository.get(mention_id)
            if not existing_mention:
                raise NotFoundException()
            result = await self.mention_repository.delete(mention_id)
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during mention deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)

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
