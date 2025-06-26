from core.entities.filters import DomainFilters


class TestDomainFilters:
    """Unit tests for the DomainFilters class."""

    def test_to_orm_dict_with_id(self):
        """Test that the id filter is correctly converted to an ORM dictionary."""
        # Given
        filters = DomainFilters(id=1)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"id": 1}

    def test_to_orm_dict_with_name(self):
        """Test that the name filter is correctly converted to an ORM dictionary."""
        # Given
        filters = DomainFilters(name="Science")

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"name__icontains": "Science"}

    def test_to_orm_dict_with_created_by(self):
        """Test that the created_by filter is correctly converted to an ORM dictionary."""
        # Given
        filters = DomainFilters(created_by=1)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"created_by": 1}

    def test_to_orm_dict_with_updated_by(self):
        """Test that the updated_by filter is correctly converted to an ORM dictionary."""
        # Given
        filters = DomainFilters(updated_by=1)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"updated_by": 1}

    def test_to_orm_dict_with_all_filters(self):
        """Test that all filters are correctly converted to an ORM dictionary."""
        # Given
        filters = DomainFilters(id=1, name="Science", created_by=1, updated_by=1)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {
            "id": 1,
            "name__icontains": "Science",
            "created_by": 1,
            "updated_by": 1,
        }

    def test_to_orm_dict_with_no_filters(self):
        """Test that an empty dictionary is returned when no filters are provided."""
        # Given
        filters = DomainFilters()

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {}

    def test_str_representation(self):
        """Test the string representation of the filters."""
        # Given
        filters = DomainFilters(id=1, name="Science")

        # When
        str_representation = str(filters)

        # Then
        assert str_representation == "DomainFilters(id=1, name__icontains=Science)"

    def test_to_orm_dict_with_created_at_after(self):
        """Test that the created_at_after filter is correctly converted."""
        # Given
        from datetime import datetime

        date = datetime.now()
        filters = DomainFilters(created_at_after=date)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"created_at__gte": date}

    def test_to_orm_dict_with_created_at_before(self):
        """Test that the created_at_before filter is correctly converted."""
        # Given
        from datetime import datetime

        date = datetime.now()
        filters = DomainFilters(created_at_before=date)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"created_at__lte": date}

    def test_to_orm_dict_with_updated_at_after(self):
        """Test that the updated_at_after filter is correctly converted."""
        # Given
        from datetime import datetime

        date = datetime.now()
        filters = DomainFilters(updated_at_after=date)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"updated_at__gte": date}

    def test_to_orm_dict_with_updated_at_before(self):
        """Test that the updated_at_before filter is correctly converted."""
        # Given
        from datetime import datetime

        date = datetime.now()
        filters = DomainFilters(updated_at_before=date)

        # When
        orm_dict = filters.to_orm_dict()

        # Then
        assert orm_dict == {"updated_at__lte": date}
