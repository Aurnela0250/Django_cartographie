from typing import Optional

from apps.city.models import City
from core.domain.entities.city_entity import CityEntity
from core.interfaces.city_repository import ICityRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository
from infrastructure.db.django_model_to_entity import city_to_entity


class DjangoCityRepository(
    DjangoBaseRepository[CityEntity, City, int], ICityRepository
):
    """Implémentation Django du repository pour les villes"""

    def __init__(self):
        super().__init__(City, CityEntity)

    def _to_entity(self, db_obj: City) -> CityEntity:
        """Convertit un objet City Django en CityEntity"""
        return city_to_entity(db_obj)

    def get_by_name(self, name: str) -> Optional[CityEntity]:
        """Récupère une ville par son nom"""
        try:
            city = self.model.objects.get(name=name)
            return self._to_entity(city)
        except self.model.DoesNotExist:
            return None
