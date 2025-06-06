"""Tests for `monggregate.operators.arithmetic.divide` module."""

from monggregate.operators.arithmetic.divide import Divide


class TestDivide:
    """Tests for `Divide` class."""

    def test_instantiation(self) -> None:
        """Test that `Divide` class can be instantiated."""
        divide_op = Divide(numerator=10, denominator=2)
        assert isinstance(divide_op, Divide)

    def test_expression(self) -> None:
        """Test that `Divide` class returns the correct expression."""
        divide_op = Divide(numerator=10, denominator=2)
        assert divide_op.expression == {"$divide": [10, 2]}
