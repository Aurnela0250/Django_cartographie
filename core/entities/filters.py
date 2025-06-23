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
            orm_dict["name__icontains"] = self.name
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


class CityFilters(BaseModel):
    """
    Filtres disponibles pour les villes avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche de villes,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(default=None, description="ID exact de la ville")
    name: Optional[str] = Field(default=None, description="Nom exact de la ville")
    region_id: Optional[int] = Field(
        default=None, description="ID de la région de la ville"
    )

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
        default=None, description="ID de l'utilisateur qui a créé la ville"
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié la ville en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Villes créées après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Villes créées avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Villes modifiées après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Villes modifiées avant cette date"
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
        if self.region_id is not None:
            orm_dict["region_id"] = self.region_id
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
        return f"CityFilters({', '.join(active_filters)})"


class EstablishmentFilters(BaseModel):
    """
    Filtres disponibles pour les établissements avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche d'établissements,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(
        default=None,
        description="ID exact de l'établissement",
    )
    name: Optional[str] = Field(
        default=None,
        description="Nom exact de l'établissement",
    )
    acronym: Optional[str] = Field(
        default=None,
        description="Acronyme exact de l'établissement",
    )
    establishment_type_id: Optional[int] = Field(
        default=None,
        description="ID du type d'établissement",
    )
    city_id: Optional[int] = Field(
        default=None,
        description="ID de la ville de l'établissement",
    )

    # Filtres de recherche textuelle
    name_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans le nom (insensible à la casse)",
    )
    name_starts_with: Optional[str] = Field(
        default=None,
        description="Nom commençant par cette chaîne",
    )
    name_ends_with: Optional[str] = Field(
        default=None,
        description="Nom se terminant par cette chaîne",
    )
    acronym_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans l'acronyme (insensible à la casse)",
    )
    address_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans l'adresse (insensible à la casse)",
    )
    description_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans la description (insensible à la casse)",
    )

    # Filtres géographiques
    has_coordinates: Optional[bool] = Field(
        default=None,
        description="Établissements avec ou sans coordonnées GPS",
    )
    latitude_min: Optional[float] = Field(
        default=None,
        description="Latitude minimum",
    )
    latitude_max: Optional[float] = Field(
        default=None,
        description="Latitude maximum",
    )
    longitude_min: Optional[float] = Field(
        default=None,
        description="Longitude minimum",
    )
    longitude_max: Optional[float] = Field(
        default=None,
        description="Longitude maximum",
    )

    # Filtres sur les données optionnelles
    has_website: Optional[bool] = Field(
        default=None,
        description="Établissements avec ou sans site web",
    )
    has_description: Optional[bool] = Field(
        default=None,
        description="Établissements avec ou sans description",
    )
    has_contacts: Optional[bool] = Field(
        default=None,
        description="Établissements avec ou sans contacts",
    )

    # Filtres sur les utilisateurs
    created_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a créé l'établissement",
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié l'établissement en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None,
        description="Établissements créés après cette date",
    )
    created_at_before: Optional[datetime] = Field(
        default=None,
        description="Établissements créés avant cette date",
    )
    updated_at_after: Optional[datetime] = Field(
        default=None,
        description="Établissements modifiés après cette date",
    )
    updated_at_before: Optional[datetime] = Field(
        default=None,
        description="Établissements modifiés avant cette date",
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

        # Filtres de base
        if self.id is not None:
            orm_dict["id"] = self.id
        if self.name is not None:
            orm_dict["name__icontains"] = self.name
        if self.acronym is not None:
            orm_dict["acronym"] = self.acronym
        if self.establishment_type_id is not None:
            orm_dict["establishment_type_id"] = self.establishment_type_id
        if self.city_id is not None:
            orm_dict["city_id"] = self.city_id

        # Filtres de recherche textuelle
        if self.name_contains is not None:
            orm_dict["name__icontains"] = self.name_contains
        if self.name_starts_with is not None:
            orm_dict["name__startswith"] = self.name_starts_with
        if self.name_ends_with is not None:
            orm_dict["name__endswith"] = self.name_ends_with
        if self.acronym_contains is not None:
            orm_dict["acronym__icontains"] = self.acronym_contains
        if self.address_contains is not None:
            orm_dict["address__icontains"] = self.address_contains
        if self.description_contains is not None:
            orm_dict["description__icontains"] = self.description_contains

        # Filtres géographiques
        if self.has_coordinates is not None:
            if self.has_coordinates:
                orm_dict["latitude__isnull"] = False
                orm_dict["longitude__isnull"] = False
            else:
                orm_dict["latitude__isnull"] = True
        if self.latitude_min is not None:
            orm_dict["latitude__gte"] = self.latitude_min
        if self.latitude_max is not None:
            orm_dict["latitude__lte"] = self.latitude_max
        if self.longitude_min is not None:
            orm_dict["longitude__gte"] = self.longitude_min
        if self.longitude_max is not None:
            orm_dict["longitude__lte"] = self.longitude_max

        # Filtres sur les données optionnelles
        if self.has_website is not None:
            orm_dict["website__isnull"] = not self.has_website
        if self.has_description is not None:
            orm_dict["description__isnull"] = not self.has_description
        if self.has_contacts is not None:
            orm_dict["contacts__isnull"] = not self.has_contacts

        # Filtres sur les utilisateurs
        if self.created_by is not None:
            orm_dict["created_by"] = self.created_by
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by

        # Filtres de date
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
        return f"EstablishmentFilters({', '.join(active_filters)})"


class EstablishmentTypeFilters(BaseModel):
    """
    Filtres disponibles pour les types d'établissements avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche de types d'établissements,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(
        default=None, description="ID exact du type d'établissement"
    )
    name: Optional[str] = Field(
        default=None, description="Nom exact du type d'établissement"
    )

    # Filtres de recherche textuelle
    name_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans le nom (insensible à la casse)",
    )
    name_starts_with: Optional[str] = Field(
        default=None,
        description="Nom commençant par cette chaîne",
    )
    name_ends_with: Optional[str] = Field(
        default=None,
        description="Nom se terminant par cette chaîne",
    )
    description_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans la description (insensible à la casse)",
    )

    # Filtres sur les données optionnelles
    has_description: Optional[bool] = Field(
        default=None,
        description="Types d'établissements avec ou sans description",
    )

    # Filtres sur les utilisateurs
    created_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a créé le type d'établissement",
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié le type d'établissement en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Types d'établissements créés après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Types d'établissements créés avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Types d'établissements modifiés après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Types d'établissements modifiés avant cette date"
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

        # Filtres de base
        if self.id is not None:
            orm_dict["id"] = self.id
        if self.name is not None:
            orm_dict["name__icontains"] = self.name

        # Filtres de recherche textuelle
        if self.name_contains is not None:
            orm_dict["name__icontains"] = self.name_contains
        if self.name_starts_with is not None:
            orm_dict["name__startswith"] = self.name_starts_with
        if self.name_ends_with is not None:
            orm_dict["name__endswith"] = self.name_ends_with
        if self.description_contains is not None:
            orm_dict["description__icontains"] = self.description_contains

        # Filtres sur les données optionnelles
        if self.has_description is not None:
            orm_dict["description__isnull"] = not self.has_description

        # Filtres sur les utilisateurs
        if self.created_by is not None:
            orm_dict["created_by"] = self.created_by
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by

        # Filtres de date
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
        return f"EstablishmentTypeFilters({', '.join(active_filters)})"


class FormationFilters(BaseModel):
    """
    Filtres disponibles pour les formations avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche de formations,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(default=None, description="ID exact de la formation")
    name: Optional[str] = Field(default=None, description="Nom exact de la formation")
    duration: Optional[int] = Field(
        default=None, description="Durée exacte de la formation"
    )
    level_id: Optional[int] = Field(
        default=None, description="ID du niveau de la formation"
    )
    mention_id: Optional[int] = Field(
        default=None, description="ID de la mention de la formation"
    )
    establishment_id: Optional[int] = Field(
        default=None, description="ID de l'établissement de la formation"
    )
    authorization_id: Optional[int] = Field(
        default=None, description="ID de l'autorisation de la formation"
    )

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
    description_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans la description (insensible à la casse)",
    )

    # Filtres sur la durée
    duration_min: Optional[int] = Field(
        default=None, description="Durée minimum de la formation"
    )
    duration_max: Optional[int] = Field(
        default=None, description="Durée maximum de la formation"
    )

    # Filtres sur les données optionnelles
    has_description: Optional[bool] = Field(
        default=None, description="Formations avec ou sans description"
    )
    has_authorization: Optional[bool] = Field(
        default=None, description="Formations avec ou sans autorisation"
    )

    # Filtres sur les utilisateurs
    created_by: Optional[int] = Field(
        default=None, description="ID de l'utilisateur qui a créé la formation"
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié la formation en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Formations créées après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Formations créées avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Formations modifiées après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Formations modifiées avant cette date"
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

        # Filtres de base
        if self.id is not None:
            orm_dict["id"] = self.id
        if self.name is not None:
            orm_dict["name"] = self.name
        if self.duration is not None:
            orm_dict["duration"] = self.duration
        if self.level_id is not None:
            orm_dict["level_id"] = self.level_id
        if self.mention_id is not None:
            orm_dict["mention_id"] = self.mention_id
        if self.establishment_id is not None:
            orm_dict["establishment_id"] = self.establishment_id
        if self.authorization_id is not None:
            orm_dict["authorization_id"] = self.authorization_id

        # Filtres de recherche textuelle
        if self.name_contains is not None:
            orm_dict["name__icontains"] = self.name_contains
        if self.name_starts_with is not None:
            orm_dict["name__startswith"] = self.name_starts_with
        if self.name_ends_with is not None:
            orm_dict["name__endswith"] = self.name_ends_with
        if self.description_contains is not None:
            orm_dict["description__icontains"] = self.description_contains

        # Filtres sur la durée
        if self.duration_min is not None:
            orm_dict["duration__gte"] = self.duration_min
        if self.duration_max is not None:
            orm_dict["duration__lte"] = self.duration_max

        # Filtres sur les données optionnelles
        if self.has_description is not None:
            orm_dict["description__isnull"] = not self.has_description
        if self.has_authorization is not None:
            orm_dict["authorization_id__isnull"] = not self.has_authorization

        # Filtres sur les utilisateurs
        if self.created_by is not None:
            orm_dict["created_by"] = self.created_by
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by

        # Filtres de date
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
        return f"FormationFilters({', '.join(active_filters)})"


class LevelFilters(BaseModel):
    """
    Filtres disponibles pour les niveaux avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche de niveaux,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(default=None, description="ID exact du niveau")
    name: Optional[str] = Field(default=None, description="Nom exact du niveau")
    acronym: Optional[str] = Field(default=None, description="Acronyme exact du niveau")

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
    acronym_contains: Optional[str] = Field(
        default=None,
        description="Recherche partielle dans l'acronyme (insensible à la casse)",
    )

    # Filtres sur les données optionnelles
    has_acronym: Optional[bool] = Field(
        default=None, description="Niveaux avec ou sans acronyme"
    )

    # Filtres sur les utilisateurs
    created_by: Optional[int] = Field(
        default=None, description="ID de l'utilisateur qui a créé le niveau"
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié le niveau en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Niveaux créés après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Niveaux créés avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Niveaux modifiés après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Niveaux modifiés avant cette date"
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

        # Filtres de base
        if self.id is not None:
            orm_dict["id"] = self.id
        if self.name is not None:
            orm_dict["name"] = self.name
        if self.acronym is not None:
            orm_dict["acronym"] = self.acronym

        # Filtres de recherche textuelle
        if self.name_contains is not None:
            orm_dict["name__icontains"] = self.name_contains
        if self.name_starts_with is not None:
            orm_dict["name__startswith"] = self.name_starts_with
        if self.name_ends_with is not None:
            orm_dict["name__endswith"] = self.name_ends_with
        if self.acronym_contains is not None:
            orm_dict["acronym__icontains"] = self.acronym_contains

        # Filtres sur les données optionnelles
        if self.has_acronym is not None:
            orm_dict["acronym__isnull"] = not self.has_acronym

        # Filtres sur les utilisateurs
        if self.created_by is not None:
            orm_dict["created_by"] = self.created_by
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by

        # Filtres de date
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
        return f"LevelFilters({', '.join(active_filters)})"


class MentionFilters(BaseModel):
    """
    Filtres disponibles pour les mentions avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche de mentions,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(default=None, description="ID exact de la mention")
    name: Optional[str] = Field(default=None, description="Nom exact de la mention")
    domain_id: Optional[int] = Field(
        default=None, description="ID du domaine de la mention"
    )

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
        default=None, description="ID de l'utilisateur qui a créé la mention"
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié la mention en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Mentions créées après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Mentions créées avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Mentions modifiées après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Mentions modifiées avant cette date"
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

        # Filtres de base
        if self.id is not None:
            orm_dict["id"] = self.id
        if self.name is not None:
            orm_dict["name"] = self.name
        if self.domain_id is not None:
            orm_dict["domain_id"] = self.domain_id

        # Filtres de recherche textuelle
        if self.name_contains is not None:
            orm_dict["name__icontains"] = self.name_contains
        if self.name_starts_with is not None:
            orm_dict["name__startswith"] = self.name_starts_with
        if self.name_ends_with is not None:
            orm_dict["name__endswith"] = self.name_ends_with

        # Filtres sur les utilisateurs
        if self.created_by is not None:
            orm_dict["created_by"] = self.created_by
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by

        # Filtres de date
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
        return f"MentionFilters({', '.join(active_filters)})"


class RegionFilters(BaseModel):
    """
    Filtres disponibles pour les régions avec validation Pydantic

    Cette classe définit tous les filtres possibles pour la recherche de régions,
    avec validation automatique des types et conversion vers les filtres ORM.
    """

    # Filtres de base
    id: Optional[int] = Field(default=None, description="ID exact de la région")
    name: Optional[str] = Field(default=None, description="Nom exact de la région")

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
        default=None, description="ID de l'utilisateur qui a créé la région"
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID de l'utilisateur qui a modifié la région en dernier",
    )

    # Filtres de date
    created_at_after: Optional[datetime] = Field(
        default=None, description="Régions créées après cette date"
    )
    created_at_before: Optional[datetime] = Field(
        default=None, description="Régions créées avant cette date"
    )
    updated_at_after: Optional[datetime] = Field(
        default=None, description="Régions modifiées après cette date"
    )
    updated_at_before: Optional[datetime] = Field(
        default=None, description="Régions modifiées avant cette date"
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

        # Filtres de base
        if self.id is not None:
            orm_dict["id"] = self.id
        if self.name is not None:
            orm_dict["name"] = self.name

        # Filtres de recherche textuelle
        if self.name_contains is not None:
            orm_dict["name__icontains"] = self.name_contains
        if self.name_starts_with is not None:
            orm_dict["name__startswith"] = self.name_starts_with
        if self.name_ends_with is not None:
            orm_dict["name__endswith"] = self.name_ends_with

        # Filtres sur les utilisateurs
        if self.created_by is not None:
            orm_dict["created_by"] = self.created_by
        if self.updated_by is not None:
            orm_dict["updated_by"] = self.updated_by

        # Filtres de date
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
        return f"RegionFilters({', '.join(active_filters)})"
