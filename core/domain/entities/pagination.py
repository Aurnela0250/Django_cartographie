from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Paramètres de pagination pour les couches internes."""

    page: int = Field(default=1, ge=1, description="Numéro de la page demandée")
    per_page: int = Field(
        default=10, ge=1, le=100, description="Nombre d'éléments par page"
    )

    @property
    def offset(self) -> int:
        """Calcule l'offset pour la requête SQL."""
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        """Retourne la limite pour la requête SQL."""
        return self.per_page


class PaginatedResult(BaseModel, Generic[T]):
    """Résultat paginé retourné par le Repository et le Use Case."""

    items: List[T]
    total_items: int
    page: int
    per_page: int
    total_pages: int
    next_page: Optional[int] = None
    previous_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
