"""Tests for `monggregate.operators.accumulators.count` module."""

from monggregate.operators.accumulators.count import Count


class TestCount:
    """Tests for `Count` class."""

    def test_instantiation(self) -> None:
        """Test that `Count` class can be instantiated."""
        count_op = Count()
        assert isinstance(count_op, Count)

    def test_expression(self) -> None:
        """Test that `Count` class returns the correct expression."""
        count_op = Count()
        assert count_op.expression == {"$count": {}}
