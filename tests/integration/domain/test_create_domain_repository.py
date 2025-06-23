import pytest

from core.container.container import Container
from core.interfaces.domain_repository import IDomainRepository
from core.interfaces.user_repository import IUserRepository
from presentation.exceptions import DatabaseIntegrityException
from tests.factories import DomainFactory, UserFactory

pytestmark = pytest.mark.integration


async def test_create_and_get_domain(container: Container):
    """
    Test de la création et de la récupération d'un domaine pour valider
    l'interaction correcte avec la base de données.
    """
    # Récupération des repositories depuis le conteneur injecté
    domain_repository: IDomainRepository = container.domain_repository()
    user_repository: IUserRepository = container.user_repository()

    # 1. Créer un utilisateur prérequis
    user_entity = UserFactory.build()
    created_user = await user_repository.create(user_entity)
    assert created_user.id is not None

    # 2. Créer une entité de domaine en liant l'utilisateur créé
    domain_entity = DomainFactory.build(
        created_by=created_user.id,
        updated_by=created_user.id,
    )

    # 3. Créer le domaine dans la base de données
    created_domain = await domain_repository.create(domain_entity)
    assert created_domain.id is not None
    assert created_domain.name == domain_entity.name
    assert created_domain.created_by == created_user.id

    # 4. Récupérer le domaine par son ID en utilisant la méthode 'get'
    retrieved_domain = await domain_repository.get(created_domain.id)

    # 5. Valider que les données récupérées sont correctes
    assert retrieved_domain is not None
    assert retrieved_domain.id == created_domain.id
    assert retrieved_domain.name == created_domain.name
    assert retrieved_domain.created_by == created_user.id


async def test_create_domain_with_existing_name_raises_error(container: Container):
    """
    Vérifie qu'une IntegrityError est levée lors de la tentative de création
    d'un domaine avec un nom qui existe déjà.
    """
    domain_repository: IDomainRepository = container.domain_repository()
    user_repository: IUserRepository = container.user_repository()

    # 1. Créer un utilisateur et un premier domaine
    user_entity = UserFactory.build()
    created_user = await user_repository.create(user_entity)
    domain_entity = DomainFactory.build(
        created_by=created_user.id, updated_by=created_user.id
    )
    await domain_repository.create(domain_entity)

    # 2. Tenter de créer un autre domaine avec le même nom
    duplicate_domain_entity = DomainFactory.build(
        name=domain_entity.name,  # Utilise le même nom
        created_by=created_user.id,
        updated_by=created_user.id,
    )

    # 3. Vérifier qu'une DatabaseIntegrityException est levée
    with pytest.raises(DatabaseIntegrityException):
        await domain_repository.create(duplicate_domain_entity)


async def test_create_domain_with_non_existing_user_raises_integrity_error(
    container: Container,
):
    """
    Vérifie qu'une IntegrityError est levée lors de la tentative de création
    d'un domaine avec un created_by qui ne correspond à aucun utilisateur.
    """
    domain_repository: IDomainRepository = container.domain_repository()

    # 1. Créer une entité de domaine avec un ID utilisateur non existant
    non_existing_user_id = 999999
    domain_entity = DomainFactory.build(
        created_by=non_existing_user_id, updated_by=non_existing_user_id
    )

    # 2. Vérifier qu'une DatabaseIntegrityException est levée
    with pytest.raises(DatabaseIntegrityException):
        await domain_repository.create(domain_entity)
