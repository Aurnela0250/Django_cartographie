from typing import Callable, Generic, List, Optional, Type, TypeVar

from ninja import Schema
from pydantic import BaseModel, ConfigDict, Field

from core.domain.entities.pagination import PaginatedResult

T = TypeVar("T")
E = TypeVar("E")


class PaginationParamsSchema(Schema):
    """Schéma pour les paramètres de pagination dans les requêtes API."""

    page: int = Field(1, ge=1, description="Numéro de la page (commence à 1)")
    per_page: int = Field(
        10, ge=1, le=100, description="Nombre d'éléments par page (max 100)"
    )

    model_config = ConfigDict(from_attributes=True)


class PaginatedResultSchema(BaseModel, Generic[T]):
    """Schéma générique pour les réponses API paginées."""

    items: List[T] = Field(
        ..., description="La liste des éléments pour la page courante"
    )
    total_items: int = Field(..., description="Nombre total d'éléments disponibles")
    page: int = Field(..., description="Le numéro de la page actuelle")
    per_page: int = Field(..., description="Le nombre d'éléments par page demandé")
    total_pages: int = Field(..., description="Le nombre total de pages")
    next_page: Optional[int] = Field(
        None, description="Le numéro de la page suivante, si elle existe"
    )
    previous_page: Optional[int] = Field(
        None, description="Le numéro de la page précédente, si elle existe"
    )

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_domain_result(
        result: PaginatedResult[T],
        schema_type: Type[E],
        item_converter: Callable[[T], E] = lambda x: x,
    ) -> "PaginatedResultSchema[E]":
        """Convertit un PaginatedResult du domaine en PaginatedResultSchema pour l'API.

        Args:
            result: Le résultat paginé du domaine à convertir
            schema_type: Le type de schéma pour les éléments de la liste
            item_converter: Fonction de conversion pour chaque élément (par défaut: identité)

        Returns:
            Un PaginatedResultSchema typé avec le schema_type fourni
        """
        return PaginatedResultSchema[schema_type](
            items=[item_converter(item) for item in result.items],
            total_items=result.total_items,
            page=result.page,
            per_page=result.per_page,
            total_pages=result.total_pages,
            next_page=result.next_page,
            previous_page=result.previous_page,
        )
