import logging

from tortoise.transactions import atomic

from core.entities.domain import DomainEntity
from core.entities.filters import DomainFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.domain_repository import IDomainRepository
from presentation.exceptions import (
    ConflictException,
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
    InternalServerErrorException,
    NotFoundException,
)


class DomainUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les domaines"""

    def __init__(
        self,
        domain_repository: IDomainRepository,
    ):
        self.domain_repository = domain_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(self, domain_data: DomainEntity) -> DomainEntity:
        try:
            return await self.domain_repository.create(domain_data)
        except DatabaseIntegrityException as e:
            self.logger.warning(
                f"Conflict creating domain with name '{domain_data.name}': {e}"
            )
            raise ConflictException(cause=e)
        except DatabaseException as e:
            self.logger.error(f"Database error during domain creation: {e}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during domain creation: {e}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, domain_id: int) -> DomainEntity:
        try:
            return await self.domain_repository.get(domain_id)
        except DatabaseDoesNotExistException as e:
            raise NotFoundException(cause=e)
        except DatabaseException as e:
            self.logger.error(f"Database error during domain retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during domain retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self,
        domain_id: int,
        domain_data: dict,
        user_id: int,
    ) -> DomainEntity:
        try:
            existing_domain = await self.domain_repository.get(domain_id)
            domain_data.update(
                {
                    "id": existing_domain.id,
                    "created_by": existing_domain.created_by,
                    "updated_by": user_id,
                    "created_at": existing_domain.created_at,
                }
            )
            domain_to_entity = DomainEntity(**domain_data)

            return await self.domain_repository.update(domain_id, domain_to_entity)

        except DatabaseDoesNotExistException as e:
            raise NotFoundException(cause=e)
        except DatabaseIntegrityException as e:
            self.logger.warning(
                f"A domain with name '{domain_data.get('name')}' may already exist."
            )
            raise ConflictException(cause=e)
        except DatabaseException as e:
            self.logger.error(f"Database error during domain retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during domain update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, domain_id: int) -> bool:
        try:
            return await self.domain_repository.delete(domain_id)
        except DatabaseDoesNotExistException as e:
            raise NotFoundException(cause=e)
        except DatabaseException as e:
            self.logger.error(f"Database error during domain deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during domain deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[DomainEntity]:
        try:
            domains = await self.domain_repository.get_all(
                pagination_params=pagination_params
            )
            return domains
        except DatabaseException as e:
            self.logger.error(f"Database error during domain retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during domains retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: DomainFilters,
    ) -> PaginatedResult[DomainEntity]:
        try:
            domains = await self.domain_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return domains
        except DatabaseException as e:
            self.logger.error(f"Database error during domains filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during domains filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
