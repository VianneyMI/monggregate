"""Tests for `monggregate.operators.arithmetic.pow` module."""

from monggregate.operators.arithmetic.pow import Pow

def test_pow_expression():
    # Setup
    number = 2
    exponent = 3
    expected_expression = {"$pow": [number, exponent]}

    # Act
    pow_op = Pow(number=number, exponent=exponent)
    result_expression = pow_op.expression

    # Assert
    assert result_expression == expected_expression


class TestPow:
    """Tests for `Pow` class."""

    def test_instantiation(self) -> None:
        """Test that `Pow` class can be instantiated."""
        pow_op = Pow(number=2, exponent=3)
        assert isinstance(pow_op, Pow)

    def test_expression(self) -> None:
        """Test that `Pow` class returns the correct expression."""
        pow_op = Pow(number=2, exponent=3)
        assert pow_op.expression == {"$pow": [2, 3]}
