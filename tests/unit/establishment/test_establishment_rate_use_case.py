from unittest.mock import AsyncMock

import pytest

from core.entities.rate import RateEntity
from core.interfaces.establishment_repository import IEstablishmentRepository
from core.interfaces.rate_repository import IRateRepository
from core.use_cases.establishment_use_case import EstablishmentUseCase
from presentation.exceptions import InternalServerErrorException


@pytest.fixture
def mock_establishment_repository():
    """Mock du repository d'établissement avec spec strict"""
    return AsyncMock(spec=IEstablishmentRepository)


@pytest.fixture
def mock_rate_repository():
    """Mock du repository de note avec spec strict"""
    return AsyncMock(spec=IRateRepository)


@pytest.fixture
def establishment_use_case(mock_establishment_repository, mock_rate_repository):
    """Fixture pour créer une instance de EstablishmentUseCase avec des mocks"""
    return EstablishmentUseCase(
        establishment_repository=mock_establishment_repository,
        rate_repository=mock_rate_repository,
    )


@pytest.fixture
def rate_factory():
    """Factory pour créer des entités RateEntity avec des valeurs par défaut"""

    def _factory(**overrides):
        defaults = {
            "id": None,
            "establishment_id": 1,
            "user_id": 1,
            "rating": 3.0,
            "created_at": None,
            "updated_at": None,
        }
        return RateEntity(**{**defaults, **overrides})

    return _factory


class TestEstablishmentRateUseCase:
    """Unit tests for the rate_establishment method of EstablishmentUseCase"""

    class TestSuccess:
        """Tests for success cases"""

        @pytest.mark.asyncio
        async def test_should_create_rate_successfully(
            self, establishment_use_case, mock_rate_repository, rate_factory
        ):
            """Test for successful rate creation"""
            # Given
            user_id = 1
            establishment_id = 1
            rating = 4.5
            new_rate_entity = rate_factory(
                user_id=user_id, establishment_id=establishment_id, rating=rating
            )
            created_rate_entity = rate_factory(
                id=1, user_id=user_id, establishment_id=establishment_id, rating=rating
            )

            mock_rate_repository.get_rate_by_user_for_establishment.return_value = None
            mock_rate_repository.create.return_value = created_rate_entity

            # When
            result = await establishment_use_case.rate_establishment(
                user_id, establishment_id, rating
            )

            # Then
            assert result == created_rate_entity
            mock_rate_repository.get_rate_by_user_for_establishment.assert_called_once_with(
                user_id=user_id, establishment_id=establishment_id
            )
            mock_rate_repository.create.assert_called_once_with(new_rate_entity)
            mock_rate_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_update_rate_successfully(
            self, establishment_use_case, mock_rate_repository, rate_factory
        ):
            """Test for successful rate update"""
            # Given
            user_id = 1
            establishment_id = 1
            initial_rating = 3.0
            new_rating = 4.0
            existing_rate_entity = rate_factory(
                id=1,
                user_id=user_id,
                establishment_id=establishment_id,
                rating=initial_rating,
            )
            updated_rate_entity = rate_factory(
                id=1,
                user_id=user_id,
                establishment_id=establishment_id,
                rating=new_rating,
            )

            mock_rate_repository.get_rate_by_user_for_establishment.return_value = (
                existing_rate_entity
            )
            mock_rate_repository.update.return_value = updated_rate_entity

            # When
            result = await establishment_use_case.rate_establishment(
                user_id, establishment_id, new_rating
            )

            # Then
            assert result == updated_rate_entity
            mock_rate_repository.get_rate_by_user_for_establishment.assert_called_once_with(
                user_id=user_id, establishment_id=establishment_id
            )
            mock_rate_repository.update.assert_called_once_with(
                existing_rate_entity.id, existing_rate_entity
            )
            mock_rate_repository.create.assert_not_called()

    class TestFailures:
        """Tests for failure cases"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_rate_failure(
            self, establishment_use_case, mock_rate_repository
        ):
            """Test for error handling during rate retrieval"""
            # Given
            user_id = 1
            establishment_id = 1
            rating = 4.0
            mock_rate_repository.get_rate_by_user_for_establishment.side_effect = (
                Exception("Database error")
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.rate_establishment(
                    user_id, establishment_id, rating
                )

            mock_rate_repository.get_rate_by_user_for_establishment.assert_called_once_with(
                user_id=user_id, establishment_id=establishment_id
            )
            mock_rate_repository.create.assert_not_called()
            mock_rate_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_create_rate_failure(
            self, establishment_use_case, mock_rate_repository, rate_factory
        ):
            """Test for error handling during rate creation"""
            # Given
            user_id = 1
            establishment_id = 1
            rating = 4.0
            new_rate_entity = rate_factory(
                user_id=user_id, establishment_id=establishment_id, rating=rating
            )

            mock_rate_repository.get_rate_by_user_for_establishment.return_value = None
            mock_rate_repository.create.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.rate_establishment(
                    user_id, establishment_id, rating
                )

            mock_rate_repository.get_rate_by_user_for_establishment.assert_called_once_with(
                user_id=user_id, establishment_id=establishment_id
            )
            mock_rate_repository.create.assert_called_once_with(new_rate_entity)
            mock_rate_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_update_rate_failure(
            self, establishment_use_case, mock_rate_repository, rate_factory
        ):
            """Test for error handling during rate update"""
            # Given
            user_id = 1
            establishment_id = 1
            initial_rating = 3.0
            new_rating = 4.0
            existing_rate_entity = rate_factory(
                id=1,
                user_id=user_id,
                establishment_id=establishment_id,
                rating=initial_rating,
            )

            mock_rate_repository.get_rate_by_user_for_establishment.return_value = (
                existing_rate_entity
            )
            mock_rate_repository.update.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.rate_establishment(
                    user_id, establishment_id, new_rating
                )

            mock_rate_repository.get_rate_by_user_for_establishment.assert_called_once_with(
                user_id=user_id, establishment_id=establishment_id
            )
            mock_rate_repository.update.assert_called_once_with(
                existing_rate_entity.id, existing_rate_entity
            )
            mock_rate_repository.create.assert_not_called()
