from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DomainFilters(BaseModel):
    """
    Filtres disponibles pour les domaines avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche de domaines,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(default=None, description="ID exact du domaine")
    name: Optional[str] = Field(default=None, description="Nom exact du domaine")

    # Filtres de recherche textuelle
    name_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans le nom (insensible à la casse)",
    )
    name_starts_with: Optional[str] = Field(
        default=None, description="Nom commençant par cette chaîne"
    )
    name_ends_with: Optional[str] = Field(
        default=None, description="Nom se terminant par cette chaîne"
    )

    # Filtres sur les utilisateurs
    created_by: Optional[int] = Field(
        default=None, description="ID de l'utilisateur qui a créé le domaine"
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié le domaine en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Domaines créés après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Domaines créés avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Domaines modifiés après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Domaines modifiés avant cette date"
    )

    class Config:
        """Configuration Pydantic"""

        use_enum_values = True

    def to_orm_dict(self) -> dict:
        """
        Convertit les filtres en dictionnaire compatible avec Tortoise ORM

        Returns:
            dict: Dictionnaire des filtres non-None avec les alias appropriés pour l'ORM
        """
        orm_dict = {}

        if self.id is not None:
            orm_dict["id"] = self.id
        if self.name is not None:
            orm_dict["name"] = self.name
        if self.name_contains is not None:
            orm_dict["name__icontains"] = self.name_contains
        if self.name_starts_with is not None:
            orm_dict["name__startswith"] = self.name_starts_with
        if self.name_ends_with is not None:
            orm_dict["name__endswith"] = self.name_ends_with
        if self.created_by is not None:
            orm_dict["created_by"] = self.created_by
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by
        if self.created_at_after is not None:
            orm_dict["created_at__gte"] = self.created_at_after
        if self.created_at_before is not None:
            orm_dict["created_at__lte"] = self.created_at_before
        if self.updated_at_after is not None:
            orm_dict["updated_at__gte"] = self.updated_at_after
        if self.updated_at_before is not None:
            orm_dict["updated_at__lte"] = self.updated_at_before

        return orm_dict

    def __str__(self) -> str:
        """Représentation string des filtres actifs"""
        active_filters = [f"{k}={v}" for k, v in self.to_orm_dict().items()]
        return f"DomainFilters({', '.join(active_filters)})"


class UserFilters(BaseModel):
    """
    Filtres disponibles pour les utilisateurs avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche d'utilisateurs,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(default=None, description="ID exact de l'utilisateur")
    email: Optional[str] = Field(
        default=None, description="Email exact de l'utilisateur"
    )
    active: Optional[bool] = Field(
        default=None, description="Statut actif de l'utilisateur"
    )
    email_verified: Optional[bool] = Field(
        default=None, description="Statut de vérification de l'email"
    )

    # Filtres de recherche textuelle sur l'email
    email_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans l'email (insensible à la casse)",
    )
    email_starts_with: Optional[str] = Field(
        default=None, description="Email commençant par cette chaîne"
    )
    email_ends_with: Optional[str] = Field(
        default=None, description="Email se terminant par cette chaîne"
    )
    email_domain: Optional[str] = Field(
        default=None, description="Filtrer par domaine email (ex: gmail.com)"
    )

    # Filtres sur les utilisateurs liés
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié cet utilisateur en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Utilisateurs créés après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Utilisateurs créés avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Utilisateurs modifiés après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Utilisateurs modifiés avant cette date"
    )

    class Config:
        """Configuration Pydantic"""

        use_enum_values = True

    def to_orm_dict(self) -> dict:
        """
        Convertit les filtres en dictionnaire compatible avec Tortoise ORM

        Returns:
            dict: Dictionnaire des filtres non-None avec les alias appropriés pour l'ORM
        """
        orm_dict = {}

        if self.id is not None:
            orm_dict["id"] = self.id
        if self.email is not None:
            orm_dict["email"] = self.email
        if self.active is not None:
            orm_dict["active"] = self.active
        if self.email_verified is not None:
            orm_dict["email_verified"] = self.email_verified
        if self.email_contains is not None:
            orm_dict["email__icontains"] = self.email_contains
        if self.email_starts_with is not None:
            orm_dict["email__startswith"] = self.email_starts_with
        if self.email_ends_with is not None:
            orm_dict["email__endswith"] = self.email_ends_with
        if self.email_domain is not None:
            orm_dict["email__iendswith"] = f"@{self.email_domain}"
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by
        if self.created_at_after is not None:
            orm_dict["created_at__gte"] = self.created_at_after
        if self.created_at_before is not None:
            orm_dict["created_at__lte"] = self.created_at_before
        if self.updated_at_after is not None:
            orm_dict["updated_at__gte"] = self.updated_at_after
        if self.updated_at_before is not None:
            orm_dict["updated_at__lte"] = self.updated_at_before

        return orm_dict

    def __str__(self) -> str:
        """Représentation string des filtres actifs"""
        active_filters = [f"{k}={v}" for k, v in self.to_orm_dict().items()]
        return f"UserFilters({', '.join(active_filters)})"
