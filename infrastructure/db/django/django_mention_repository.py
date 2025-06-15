from typing import Optional

from apps.domain.models import Domain
from apps.mentions.models import Mention
from core.domain.entities.mention_entity import MentionEntity
from core.interfaces.mention_repository import IMentionRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository
from presentation.exceptions import NotFoundError, UnprocessableEntityError


class DjangoMentionRepository(
    DjangoBaseRepository[MentionEntity, Mention, int],
    IMentionRepository,
):
    def __init__(self):
        super().__init__(Mention, MentionEntity)

    def check_domain_exists(self, domain_id: int) -> bool:
        """Checks if a Domain with the given ID exists."""
        return Domain.objects.filter(id=domain_id).exists()

    def create(self, mention: MentionEntity) -> MentionEntity:
        """Creates a new Mention record in the database."""
        if not self.check_domain_exists(mention.domain_id):
            raise UnprocessableEntityError()
        return super().create(mention)

    def get_by_id(self, mention_id: int) -> Optional[MentionEntity]:
        """Retrieves a Mention by its ID."""
        try:
            return self.get(mention_id)
        except NotFoundError:
            raise

    def update(
        self, mention_id: int, mention_data: MentionEntity
    ) -> Optional[MentionEntity]:
        """Updates an existing Mention."""
        if mention_data.domain_id is not None and not self.check_domain_exists(
            mention_data.domain_id
        ):
            raise UnprocessableEntityError()

        try:
            return super().update(mention_id, mention_data)
        except UnprocessableEntityError:
            raise
