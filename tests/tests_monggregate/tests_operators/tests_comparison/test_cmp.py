"""Tests for `monggregate.operators.comparison.cmp` module."""

from monggregate.operators.comparison.cmp import Compare


class TestCompare:
    """Tests for `Compare` class."""

    def test_instantiation(self) -> None:
        """Test that `Compare` class can be instantiated."""
        cmp_op = Compare(left="$field", right=10)
        assert isinstance(cmp_op, Compare)

    def test_expression(self) -> None:
        """Test that `Compare` class returns the correct expression."""
        cmp_op = Compare(left="$field", right=10)
        assert cmp_op.expression == {"$cmp": ["$field", 10]}
