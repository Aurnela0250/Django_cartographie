from core.domain.entities.city_entity import CityEntity
from core.domain.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_city_repository import DjangoCityRepository
from infrastructure.db.django_region_repository import DjangoRegionRepository
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnprocessableEntityError,
    ValidationError,
)
from presentation.schemas.city_schema import CreateCitySchemaRequest, UpdateCitySchema


class CityUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work

    def create(
        self,
        city_data: CreateCitySchemaRequest,
        created_by: int,
    ) -> CityEntity:
        with self.unit_of_work:
            try:
                city_repository = self.unit_of_work.get_repository(DjangoCityRepository)
                region_repository = self.unit_of_work.get_repository(
                    DjangoRegionRepository
                )

                # Vérifier si la région existe
                region = region_repository.get(city_data.region_id)
                if not region:
                    raise UnprocessableEntityError()

                # Vérifier si une ville avec le même nom existe déjà
                existing_city = city_repository.get_by_name(city_data.name)
                if existing_city:
                    raise ConflictError()

                city = CityEntity(**city_data.model_dump(), created_by=created_by)
                city_created = city_repository.create(city)
                return city_created
            except ConflictError as e:
                raise e
            except ValidationError as e:
                raise e
            except Exception:
                raise InternalServerError()

    def update(
        self,
        id: int,
        city_data: UpdateCitySchema,
        updated_by: int,
    ) -> CityEntity:
        with self.unit_of_work:
            try:
                city_repository = self.unit_of_work.get_repository(DjangoCityRepository)
                current_city = city_repository.get(id)

                if not current_city:
                    raise UnprocessableEntityError()

                update_data = current_city.model_dump()

                # Mettre à jour uniquement les champs non-None
                for key, value in city_data.model_dump(exclude_unset=True).items():
                    if value is not None:
                        update_data[key] = value

                # Vérifier si le nouveau nom est déjà utilisé
                if city_data.name and city_data.name != current_city.name:
                    existing_city = city_repository.get_by_name(city_data.name)
                    if existing_city and existing_city.id != id:
                        raise ConflictError()

                update_data["updated_by"] = updated_by
                updated_city = CityEntity(**update_data)
                return city_repository.update(id, updated_city)
            except NotFoundError as e:
                raise e
            except ConflictError as e:
                raise e
            except ValidationError as e:
                raise e
            except Exception:
                raise InternalServerError()

    def delete(self, id: int) -> bool:
        with self.unit_of_work:
            try:
                city_repository = self.unit_of_work.get_repository(DjangoCityRepository)
                city = city_repository.get(id)

                if not city:
                    raise NotFoundError()

                return city_repository.delete(id)
            except NotFoundError as e:
                raise e
            except Exception:
                raise InternalServerError()

    def get(self, id: int) -> CityEntity:
        try:
            city_repository = self.unit_of_work.get_repository(DjangoCityRepository)
            city = city_repository.get(id)

            if not city:
                raise NotFoundError()

            return city
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[CityEntity]:
        """
        Récupère toutes les villes avec pagination
        """
        try:
            city_repository = self.unit_of_work.get_repository(DjangoCityRepository)
            result = city_repository.get_all(pagination_params)
            return result
        except Exception:
            raise InternalServerError()
