"""Tests for `monggregate.operators.arithmetic.multiply` module."""

from monggregate.operators.arithmetic.multiply import Multiply


class TestMultiply:
    """Tests for `Multiply` class."""

    def test_instantiation(self) -> None:
        """Test that `Multiply` class can be instantiated."""
        multiply_op = Multiply(operands=[2, 3])
        assert isinstance(multiply_op, Multiply)

    def test_expression(self) -> None:
        """Test that `Multiply` class returns the correct expression."""
        multiply_op = Multiply(operands=[2, 3])
        assert multiply_op.expression == {"$multiply": [2, 3]}
