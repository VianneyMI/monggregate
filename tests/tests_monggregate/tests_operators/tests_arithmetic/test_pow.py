"""Tests for `monggregate.operators.arithmetic.pow` module."""

from monggregate.operators.arithmetic.pow import Pow


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
