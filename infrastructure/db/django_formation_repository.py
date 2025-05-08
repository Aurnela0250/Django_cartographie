# Implementation du repository Formation
from typing import Optional

from apps.establishment.models import Establishment
from apps.formation.models import Formation
from apps.formation_authorization.models import FormationAuthorization
from apps.levels.models import Level
from apps.mentions.models import Mention
from apps.users.models import User
from core.domain.entities.formation_authorization_entity import (
    FormationAuthorizationEntity,
)
from core.domain.entities.formation_entity import FormationEntity
from core.interfaces.formation_repository import IFormationRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository
from infrastructure.db.django_model_to_entity import (
    FormationToEntityMetadata,
    formation_to_entity,
)
from presentation.exceptions import UnprocessableEntityError


class DjangoFormationRepository(
    DjangoBaseRepository[FormationEntity, Formation, int],
    IFormationRepository,
):
    """Django implementation of the repository for formations"""

    def __init__(self):
        super().__init__(Formation, FormationEntity)

    def _to_entity(self, db_obj: Formation) -> FormationEntity:
        """Surcharge de la méthode _to_entity pour utiliser formation_to_entity"""
        return formation_to_entity(
            db_obj,
            metadata=FormationToEntityMetadata(
                level=True,
                mention=True,
                establishment=False,
                authorization=True,
            ),
        )

    def get_by_intitule(self, intitule: str) -> Optional[FormationEntity]:
        try:
            formation = self.model.objects.get(intitule=intitule)
            return self._to_entity(formation)
        except self.model.DoesNotExist:
            return None

    def check_level_exists(self, level_id: int) -> bool:
        return Level.objects.filter(id=level_id).exists()

    def check_mention_exists(self, mention_id: int) -> bool:
        return Mention.objects.filter(id=mention_id).exists()

    def check_establishment_exists(self, establishment_id: int) -> bool:
        return Establishment.objects.filter(id=establishment_id).exists()

    def check_formation_authorization_exists(self, authorization_id: int) -> bool:
        return FormationAuthorization.objects.filter(id=authorization_id).exists()

    def create(self, obj: FormationEntity) -> FormationEntity:
        # Validation des entités liées
        if not self.check_level_exists(obj.level_id):
            raise UnprocessableEntityError()
        if not self.check_mention_exists(obj.mention_id):
            raise UnprocessableEntityError()
        if not self.check_establishment_exists(obj.establishment_id):
            raise UnprocessableEntityError()
        if obj.authorization_id and not self.check_formation_authorization_exists(
            obj.authorization_id
        ):
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
                "level_id",
                "level",
                "mention_id",
                "mention",
                "establishment_id",
                "establishment",
                "authorization_id",
                "authorization",
            }
        )

        db_obj = self.model(**obj_dict)
        db_obj.level = Level.objects.get(id=obj.level_id)
        db_obj.mention = Mention.objects.get(id=obj.mention_id)
        db_obj.establishment = Establishment.objects.get(id=obj.establishment_id)
        if obj.authorization_id:
            db_obj.authorization = FormationAuthorization.objects.get(
                id=obj.authorization_id
            )

        if created_by_id:
            db_obj.created_by = User.objects.get(id=created_by_id)
        if updated_by_id:
            db_obj.updated_by = User.objects.get(id=updated_by_id)

        db_obj.save()
        return self._to_entity(db_obj)

    def update(self, id: int, obj: FormationEntity) -> FormationEntity:
        # Validation des entités liées
        if not self.check_level_exists(obj.level_id):
            raise UnprocessableEntityError()
        if not self.check_mention_exists(obj.mention_id):
            raise UnprocessableEntityError()
        if not self.check_establishment_exists(obj.establishment_id):
            raise UnprocessableEntityError()
        if obj.authorization_id and not self.check_formation_authorization_exists(
            obj.authorization_id
        ):
            raise UnprocessableEntityError()

        updated_by_id = obj.updated_by
        db_obj = self.model.objects.get(id=id)
        for key, value in obj.model_dump(
            exclude={
                "id",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
                "level_id",
                "level",
                "mention_id",
                "mention",
                "establishment_id",
                "establishment",
                "authorization_id",
                "authorization",
            }
        ).items():
            setattr(db_obj, key, value)

        db_obj.level = Level.objects.get(id=obj.level_id)
        db_obj.mention = Mention.objects.get(id=obj.mention_id)
        db_obj.establishment = Establishment.objects.get(id=obj.establishment_id)
        if obj.authorization_id:
            db_obj.authorization = FormationAuthorization.objects.get(
                id=obj.authorization_id
            )
        else:
            db_obj.authorization = None

        if updated_by_id:
            db_obj.updated_by = User.objects.get(id=updated_by_id)

        db_obj.save()
        return self._to_entity(db_obj)

    def create_formation_authorization(
        self,
        formation_id: int,
        authorization_entity: FormationAuthorizationEntity,
    ) -> FormationEntity:
        """
        Crée une FormationAuthorization et l'associe à la formation, puis retourne la FormationEntity enrichie (authorization=True)
        """
        formation = self.model.objects.get(id=formation_id)
        created_by_id = authorization_entity.created_by
        updated_by_id = authorization_entity.updated_by

        auth_dict = authorization_entity.model_dump(
            exclude={
                "id",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            }
        )

        authorization = FormationAuthorization.objects.create(**auth_dict)

        if created_by_id:
            authorization.created_by = User.objects.get(id=created_by_id)
        if updated_by_id:
            authorization.updated_by = User.objects.get(id=updated_by_id)
        authorization.save()

        formation.authorization = authorization
        formation.save()

        return formation_to_entity(
            formation,
            metadata=FormationToEntityMetadata(
                level=True,
                mention=True,
                establishment=False,
                authorization=True,
            ),
        )

    def update_formation_authorization(
        self,
        formation_id: int,
        authorization_entity: FormationAuthorizationEntity,
    ) -> FormationEntity:
        """
        Met à jour la FormationAuthorization associée à la formation, puis retourne la FormationEntity enrichie (authorization=True)
        """
        formation = self.model.objects.get(id=formation_id)
        authorization = formation.authorization
        if not authorization:
            raise UnprocessableEntityError()

        updated_by_id = authorization_entity.updated_by

        auth_dict = authorization_entity.model_dump(
            exclude={
                "id",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            }
        )

        for key, value in auth_dict.items():
            setattr(authorization, key, value)

        if updated_by_id:
            authorization.updated_by = User.objects.get(id=updated_by_id)

        authorization.save()

        return formation_to_entity(
            formation,
            metadata=FormationToEntityMetadata(
                level=True,
                mention=True,
                establishment=False,
                authorization=True,
            ),
        )
