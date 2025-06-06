"""Tests for `monggregate.operators.accumulators.sum` module."""

from monggregate.operators.accumulators.sum import Sum


class TestSum:
    """Tests for `Sum` class."""

    def test_instantiation(self) -> None:
        """Test that `Sum` class can be instantiated."""
        sum_op = Sum(operand=1)
        assert isinstance(sum_op, Sum)

    def test_expression(self) -> None:
        """Test that `Sum` class returns the correct expression."""
        sum_op = Sum(operand=1)
        assert sum_op.expression == {"$sum": 1}
