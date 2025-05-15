"""Tests for the Set stage."""

from monggregate.stages import Set


class TestSet:
    """Tests for the Set stage."""

    def test_instantiation(self) -> None:
        """Test that the Set stage can be instantiated correctly."""

        set = Set(document={"field1": 1, "field2": 2})
        assert isinstance(set, Set)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        set = Set(document={"field1": 1, "field2": 2})
        assert set.expression == {"$set": {"field1": 1, "field2": 2}}
