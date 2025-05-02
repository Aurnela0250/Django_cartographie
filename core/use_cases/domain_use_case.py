import logging
from typing import List

from core.domain.entities.domain_entity import DomainEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_domain_repository import DjangoDomainRepository
from presentation.exceptions import ConflictError, NotFoundError


class DomainUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les domaines"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_domain(self, domain_data: DomainEntity) -> DomainEntity:
        with self.unit_of_work:
            domain_repository = self.unit_of_work.get_repository(DjangoDomainRepository)
            existing_domain = domain_repository.get_by_name(domain_data.name)
            if existing_domain:
                self.logger.warning(
                    f"Domain with name '{domain_data.name}' already exists"
                )
                raise ConflictError()
            created_domain = domain_repository.create(domain_data)
            self.unit_of_work.commit()
            return created_domain

    def get_domain(self, domain_id: int) -> DomainEntity:
        with self.unit_of_work:
            domain_repository = self.unit_of_work.get_repository(DjangoDomainRepository)
            domain = domain_repository.get(domain_id)
            if not domain:
                raise NotFoundError()
            return domain

    def update_domain(self, domain_id: int, domain_data: DomainEntity) -> DomainEntity:
        with self.unit_of_work:
            domain_repository = self.unit_of_work.get_repository(DjangoDomainRepository)
            existing_domain = domain_repository.get(domain_id)
            if not existing_domain:
                raise NotFoundError()
            if domain_data.name != existing_domain.name:
                name_exists = domain_repository.get_by_name(domain_data.name)
                if name_exists and name_exists.id != domain_id:
                    self.logger.warning(
                        f"Cannot update: Domain with name '{domain_data.name}' already exists"
                    )
                    raise ConflictError()
            updated_domain = domain_repository.update(domain_id, domain_data)
            self.unit_of_work.commit()
            return updated_domain

    def delete_domain(self, domain_id: int) -> bool:
        with self.unit_of_work:
            domain_repository = self.unit_of_work.get_repository(DjangoDomainRepository)
            existing_domain = domain_repository.get(domain_id)
            if not existing_domain:
                raise NotFoundError()
            result = domain_repository.delete(domain_id)
            self.unit_of_work.commit()
            return result

    def get_all_domains(self) -> List[DomainEntity]:
        with self.unit_of_work:
            domain_repository = self.unit_of_work.get_repository(DjangoDomainRepository)
            return domain_repository.get_all()

    def filter_domains(self, **kwargs) -> List[DomainEntity]:
        with self.unit_of_work:
            domain_repository = self.unit_of_work.get_repository(DjangoDomainRepository)
            return domain_repository.filter(**kwargs)
