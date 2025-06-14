"""Tests for `monggregate.operators.arithmetic.multiply` module."""

from monggregate.operators.arithmetic.multiply import Multiply

def test_multiply_expression():
    # Setup
    operands = [2, 3, 4]
    expected_expression = {"$multiply": operands}

    # Act
    multiply_op = Multiply(operands=operands)
    result_expression = multiply_op.expression

    # Assert
    assert result_expression == expected_expression


class TestMultiply:
    """Tests for `Multiply` class."""

    def test_instantiation(self) -> None:
        """Test that `Multiply` class can be instantiated."""
        multiply_op = Multiply(operands=[2, 3, 4])
        assert isinstance(multiply_op, Multiply)

    def test_expression(self) -> None:
        """Test that `Multiply` class returns the correct expression."""
        multiply_op = Multiply(operands=[2, 3, 4])
        assert multiply_op.expression == {"$multiply": [2, 3, 4]}
