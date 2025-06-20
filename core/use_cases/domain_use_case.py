import logging

from tortoise.transactions import atomic

from core.entities.domain_entity import DomainEntity
from core.entities.filters import DomainFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.domain_repository import IDomainRepository
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class DomainUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les domaines"""

    def __init__(self, domain_repository: IDomainRepository):
        self.domain_repository = domain_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(self, domain_data: DomainEntity) -> DomainEntity:
        try:
            existing_domain = await self.domain_repository.get_by_name(domain_data.name)
            if existing_domain:
                self.logger.warning(
                    f"Domain with name '{domain_data.name}' already exists"
                )
                raise ConflictException()
            created_domain = await self.domain_repository.create(domain_data)
            return created_domain
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during domain creation: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, domain_id: int) -> DomainEntity:
        try:
            domain = await self.domain_repository.get(domain_id)
            if not domain:
                raise NotFoundException()
            return domain
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during domain retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(self, domain_id: int, domain_data: DomainEntity) -> DomainEntity:
        try:
            existing_domain = await self.domain_repository.get(domain_id)
            if not existing_domain:
                raise NotFoundException()
            if domain_data.name != existing_domain.name:
                name_exists = await self.domain_repository.get_by_name(domain_data.name)
                if name_exists and name_exists.id != domain_id:
                    self.logger.warning(
                        f"Cannot update: Domain with name '{domain_data.name}' already exists"
                    )
                    raise ConflictException()
            updated_domain = await self.domain_repository.update(domain_id, domain_data)
            return updated_domain
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during domain update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, domain_id: int) -> bool:
        try:
            existing_domain = await self.domain_repository.get(domain_id)
            if not existing_domain:
                raise NotFoundException()
            result = await self.domain_repository.delete(domain_id)
            return result
        except NotFoundException as e:
            raise e
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
        except Exception as e:
            self.logger.error(f"Unexpected error during domains filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
