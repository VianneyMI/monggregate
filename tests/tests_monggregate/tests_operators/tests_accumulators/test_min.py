"""Tests for `monggregate.operators.accumulators.min` module."""

from monggregate.operators.accumulators.min import Min


class TestMin:
    """Tests for `Min` class."""

    def test_instantiation(self) -> None:
        """Test that `Min` class can be instantiated."""
        min_op = Min(operand=1)
        assert isinstance(min_op, Min)

    def test_expression(self) -> None:
        """Test that `Min` class returns the correct expression."""
        min_op = Min(operand=1)
        assert min_op.expression == {"$min": 1}
