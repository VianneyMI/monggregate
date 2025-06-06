"""Tests for `monggregate.operators.arithmetic.subtract` module."""

from monggregate.operators.arithmetic.subtract import Subtract


class TestSubtract:
    """Tests for `Subtract` class."""

    def test_instantiation(self) -> None:
        """Test that `Subtract` class can be instantiated."""
        subtract_op = Subtract(left=5, right=3)
        assert isinstance(subtract_op, Subtract)

    def test_expression(self) -> None:
        """Test that `Subtract` class returns the correct expression."""
        subtract_op = Subtract(left=5, right=3)
        assert subtract_op.expression == {"$substract": [5, 3]}
