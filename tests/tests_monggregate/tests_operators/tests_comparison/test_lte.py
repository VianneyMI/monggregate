"""Tests for `monggregate.operators.comparison.lte` module."""

from monggregate.operators.comparison.lte import LowerThanOrEqual


class TestLowerThanOrEqual:
    """Tests for `LowerThanOrEqual` class."""

    def test_instantiation(self) -> None:
        """Test that `LowerThanOrEqual` class can be instantiated."""
        lte_op = LowerThanOrEqual(left="$field", right=10)
        assert isinstance(lte_op, LowerThanOrEqual)

    def test_expression(self) -> None:
        """Test that `LowerThanOrEqual` class returns the correct expression."""
        lte_op = LowerThanOrEqual(left="$field", right=10)
        assert lte_op.expression == {"$lte": ["$field", 10]}
