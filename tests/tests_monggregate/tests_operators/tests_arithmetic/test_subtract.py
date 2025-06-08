"""Tests for `monggregate.operators.arithmetic.subtract` module."""

from monggregate.operators.arithmetic.subtract import Subtract

def test_subtract_expression():
    # Setup
    left = 10
    right = 4
    expected_expression = {"$substract": [left, right]}

    # Act
    subtract_op = Subtract(left=left, right=right)
    result_expression = subtract_op.expression

    # Assert
    assert result_expression == expected_expression


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
