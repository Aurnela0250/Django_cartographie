from typing import List

from core.domain.entities.mention_entity import MentionEntity
from core.interfaces.unit_of_work import UnitOfWork
from core.domain.entities.pagination import PaginatedResult, PaginationParams
from infrastructure.db.django_mention_repository import DjangoMentionRepository
from presentation.exceptions import (
    DatabaseError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.mention_schema import CreateMentionSchema, UpdateMentionSchema


class MentionUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work

    def create(
        self, mention_data: CreateMentionSchema, created_by: int
    ) -> MentionEntity:
        """Creates a new mention."""
        try:
            data_dict = mention_data.model_dump()
            mention_entity = MentionEntity(**data_dict, created_by=created_by)

            with self.unit_of_work:
                mention_repo = self.unit_of_work.get_repository(DjangoMentionRepository)
                created_mention = mention_repo.create(mention_entity)
                self.unit_of_work.commit()
                return created_mention
        except NotFoundError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            # Log the error
            self.unit_of_work.rollback()
            raise InternalServerError()

    def get(self, mention_id: int) -> MentionEntity:
        """Retrieves a mention by its ID."""
        try:
            with self.unit_of_work:
                mention_repo = self.unit_of_work.get_repository(DjangoMentionRepository)
                mention = mention_repo.get_by_id(mention_id)
                if not mention:
                    raise NotFoundError()
                return mention
        except NotFoundError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            # Log the error
            raise InternalServerError()

    def update(
        self, mention_id: int, mention_data: UpdateMentionSchema, updated_by: int
    ) -> MentionEntity:
        """Updates an existing mention."""
        try:
            update_data_dict = mention_data.model_dump(exclude_unset=True)

            if not update_data_dict:
                raise ValidationError()

            with self.unit_of_work:
                mention_repo = self.unit_of_work.get_repository(DjangoMentionRepository)

                # Fetch existing mention to update
                existing_mention = mention_repo.get_by_id(mention_id)
                if not existing_mention:
                    raise NotFoundError()

                # Prepare update entity
                update_entity_data = existing_mention.model_dump()
                update_entity_data.update(update_data_dict)
                update_entity_data["updated_by"] = updated_by

                mention_entity_to_update = MentionEntity(**update_entity_data)

                # Domain existence check is handled within the repository update method if domain_id is updated
                updated_mention = mention_repo.update(
                    mention_id, mention_entity_to_update
                )
                if not updated_mention:
                    raise NotFoundError()

                self.unit_of_work.commit()
                return updated_mention
        except NotFoundError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            # Log the error
            self.unit_of_work.rollback()
            raise InternalServerError()

    def delete(self, mention_id: int) -> bool:
        """Deletes a mention by its ID."""
        try:
            with self.unit_of_work:
                mention_repo = self.unit_of_work.get_repository(DjangoMentionRepository)
                # On utilise la méthode delete de DjangoBaseRepository qui lève NotFoundError si non trouvé
                mention_repo.delete(
                    mention_id
                )  # Cette méthode lèvera NotFoundError si non trouvé
                self.unit_of_work.commit()
                return True
        except NotFoundError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            # Log the error
            self.unit_of_work.rollback()
            raise InternalServerError()

    def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[MentionEntity]:
        """Retrieves all mentions."""
        try:
            with self.unit_of_work:
                mention_repo = self.unit_of_work.get_repository(DjangoMentionRepository)
                mentions = mention_repo.get_all(pagination_params)
                return mentions
        except DatabaseError as e:
            raise e
        except Exception:
            # Log the error
            raise InternalServerError()
