"""Tests for the Count stage."""

from monggregate.stages import Count


class TestCount:
    """Tests for the Count stage."""

    def test_instantiation(self) -> None:
        """Test that the Count stage can be instantiated."""
        count = Count(name="count")
        assert isinstance(count, Count)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        count = Count(name="count")
        assert count.expression == {"$count": "count"}
