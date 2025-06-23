import pytest

from core.container.container import Container
from core.entities.pagination import PaginationParams
from core.interfaces.domain_repository import IDomainRepository

pytestmark = pytest.mark.integration


async def test_get_all_returns_empty_paginated_result_when_db_is_empty(
    container: Container,
) -> None:
    """
    Given: An empty database.
    When: The get_all method is called with pagination parameters.
    Then: It should return an empty PaginatedResult with correct structure.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure it's empty for this test
    from apps.tortoise.domain.models import Domain as TortoiseDomain

    await TortoiseDomain.all().delete()

    pagination_params = PaginationParams(page=1, per_page=10)

    # Act
    result = await domain_repository.get_all(pagination_params)

    # Assert
    assert result is not None
    assert result.items == []
    assert result.total_items == 0
    assert result.total_pages == 0


async def test_get_all_returns_single_page_when_domains_count_less_than_page_size(
    container: Container,
) -> None:
    """
    Given: A database with 3 domains (less than page size of 10).
    When: The get_all method is called with pagination parameters (page=1, per_page=10).
    Then: It should return a single page with 3 items and total_pages=1.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure isolation
    from apps.tortoise.domain.models import Domain as TortoiseDomain
    from apps.tortoise.user.models import User as TortoiseUser

    await TortoiseDomain.all().delete()
    await TortoiseUser.all().delete()

    # Create a user first
    user = await TortoiseUser.create(
        email="test@example.com",
        password="password123",
        active=True,
        email_verified=True,
    )

    # Create 3 domains (less than page size of 10)
    domain_names = ["Domain 1", "Domain 2", "Domain 3"]
    for name in domain_names:
        await TortoiseDomain.create(name=name, created_by_id=user.id)

    pagination_params = PaginationParams(page=1, per_page=10)

    # Act
    result = await domain_repository.get_all(pagination_params)

    # Assert
    assert result is not None
    assert len(result.items) == 3
    assert result.total_items == 3
    assert result.total_pages == 1
    assert result.page == 1
    assert result.per_page == 10
    # Verify that the domain names are in the result
    result_names = [domain.name for domain in result.items]
    for expected_name in domain_names:
        assert expected_name in result_names


async def test_get_all_pagination_works_correctly_across_multiple_pages(
    container: Container,
) -> None:
    """
    Given: A database with 12 domains and pagination with per_page=5.
    When: The get_all method is called with different page numbers.
    Then: It should return correct pagination data for each page.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure isolation
    from apps.tortoise.domain.models import Domain as TortoiseDomain
    from apps.tortoise.user.models import User as TortoiseUser

    await TortoiseDomain.all().delete()
    await TortoiseUser.all().delete()

    # Create a user first
    user = await TortoiseUser.create(
        email="test@example.com",
        password="password123",
        active=True,
        email_verified=True,
    )

    # Create 12 domains to test multi-page pagination
    domain_names = [f"Domain {i}" for i in range(1, 13)]
    for name in domain_names:
        await TortoiseDomain.create(name=name, created_by_id=user.id)

    # Act & Assert - Page 1
    pagination_params_page1 = PaginationParams(page=1, per_page=5)
    result_page1 = await domain_repository.get_all(pagination_params_page1)

    # Assertions Page 1
    assert result_page1.total_items == 12
    assert len(result_page1.items) == 5
    assert result_page1.total_pages == 3
    assert result_page1.page == 1
    assert result_page1.next_page == 2
    assert result_page1.previous_page is None

    # Act & Assert - Page 2
    pagination_params_page2 = PaginationParams(page=2, per_page=5)
    result_page2 = await domain_repository.get_all(pagination_params_page2)

    # Assertions Page 2
    assert len(result_page2.items) == 5
    assert result_page2.page == 2
    assert result_page2.next_page == 3
    assert result_page2.previous_page == 1


async def test_filter_by_exact_name_returns_single_matching_domain(
    container: Container,
) -> None:
    """
    Given: Une base de données avec plusieurs domaines aux noms distincts.
    When: La méthode filter est appelée avec un filtre de nom exact.
    Then: Elle doit retourner uniquement le domaine correspondant au nom exact.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure isolation
    from apps.tortoise.domain.models import Domain as TortoiseDomain
    from apps.tortoise.user.models import User as TortoiseUser
    from core.entities.filters import DomainFilters

    await TortoiseDomain.all().delete()
    await TortoiseUser.all().delete()

    # Create a user first
    user = await TortoiseUser.create(
        email="test@example.com",
        password="password123",
        active=True,
        email_verified=True,
    )

    # Create multiple domains with distinct names
    domain_names = ["Domaine A", "Domaine B", "Domaine C"]
    for name in domain_names:
        await TortoiseDomain.create(name=name, created_by_id=user.id)

    # Create DomainFilters object with exact name search
    filters = DomainFilters(name="Domaine B")
    pagination_params = PaginationParams(page=1, per_page=10)

    # Act
    result = await domain_repository.filter(pagination_params, filters)

    # Assert
    assert result is not None
    assert result.total_items == 1
    assert len(result.items) == 1
    assert result.items[0].name == "Domaine B"


async def test_filter_by_name_icontains_returns_matching_domains_case_insensitive(
    container: Container,
) -> None:
    """
    Given: Une base de données avec plusieurs domaines dont certains contiennent "informatique" dans leur nom.
    When: La méthode filter est appelée avec un filtre name__icontains="informatique".
    Then: Elle doit retourner tous les domaines contenant "informatique" de manière insensible à la casse.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure isolation
    from apps.tortoise.domain.models import Domain as TortoiseDomain
    from apps.tortoise.user.models import User as TortoiseUser
    from core.entities.filters import DomainFilters

    await TortoiseDomain.all().delete()
    await TortoiseUser.all().delete()

    # Create a user first
    user = await TortoiseUser.create(
        email="test@example.com",
        password="password123",
        active=True,
        email_verified=True,
    )

    # Create multiple domains with different cases containing "informatique"
    domain_names = [
        "Informatique de Gestion",
        "Génie Informatique",
        "Droit des Affaires",
    ]
    for name in domain_names:
        await TortoiseDomain.create(name=name, created_by_id=user.id)

    # Create DomainFilters object with case-insensitive name search using simplified name field
    filters = DomainFilters(name="informatiq")
    pagination_params = PaginationParams(page=1, per_page=10)

    # Act
    result = await domain_repository.filter(pagination_params, filters)

    # Assert
    assert result is not None
    assert result.total_items == 2
    assert len(result.items) == 2

    # Verify that both returned domains contain "Informatique" (case-insensitive)
    result_names = [domain.name for domain in result.items]
    informatique_domains = [
        name for name in result_names if "informatique" in name.lower()
    ]
    assert len(informatique_domains) == 2
    assert "Informatique de Gestion" in result_names
    assert "Génie Informatique" in result_names
    assert "Droit des Affaires" not in result_names


async def test_filter_returns_empty_paginated_result_when_no_domains_match_criteria(
    container: Container,
) -> None:
    """
    Given: Une base de données avec plusieurs domaines.
    When: La méthode filter est appelée avec un critère qui ne correspond à aucun domaine.
    Then: Elle doit retourner un PaginatedResult vide et correctement formaté.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure isolation
    from apps.tortoise.domain.models import Domain as TortoiseDomain
    from apps.tortoise.user.models import User as TortoiseUser
    from core.entities.filters import DomainFilters

    await TortoiseDomain.all().delete()
    await TortoiseUser.all().delete()

    # Create a user first
    user = await TortoiseUser.create(
        email="test@example.com",
        password="password123",
        active=True,
        email_verified=True,
    )

    # Create some domains
    domain_names = ["Informatique", "Médecine", "Droit"]
    for name in domain_names:
        await TortoiseDomain.create(name=name, created_by_id=user.id)

    # Create DomainFilters object with a name that doesn't match any domain
    filters = DomainFilters(name="Ce Nom N'existe Pas")
    pagination_params = PaginationParams(page=1, per_page=10)

    # Act
    result = await domain_repository.filter(pagination_params, filters)

    # Assert
    assert result is not None
    assert result.total_items == 0
    assert len(result.items) == 0
    assert result.total_pages == 0
