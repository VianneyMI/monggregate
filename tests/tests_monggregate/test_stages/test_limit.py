"""Tests for the Limit stage."""

from monggregate.stages import Limit


class TestLimit:
    """Tests for the Limit stage."""

    def test_instantiation(self) -> None:
        """Test that the Limit stage can be instantiated."""
        limit = Limit(value=10)
        assert isinstance(limit, Limit)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""
        limit = Limit(value=10)
        assert limit.expression == {"$limit": 10}
