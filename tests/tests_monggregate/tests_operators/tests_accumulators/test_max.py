"""Tests for `monggregate.operators.accumulators.max` module."""

from monggregate.operators.accumulators.max import Max


class TestMax:
    """Tests for `Max` class."""

    def test_instantiation(self) -> None:
        """Test that `Max` class can be instantiated."""
        max_op = Max(operand=1)
        assert isinstance(max_op, Max)

    def test_expression(self) -> None:
        """Test that `Max` class returns the correct expression."""
        max_op = Max(operand=1)
        assert max_op.expression == {"$max": 1}
