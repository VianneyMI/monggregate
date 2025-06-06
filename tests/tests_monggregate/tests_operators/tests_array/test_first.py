"""Tests for `monggregate.operators.array.first` module."""

from monggregate.operators.array.first import First


class TestFirst:
    """Tests for `First` class."""

    def test_instantiation(self) -> None:
        """Test that `First` class can be instantiated."""
        first_op = First(operand="$items")
        assert isinstance(first_op, First)

    def test_expression(self) -> None:
        """Test that `First` class returns the correct expression."""
        first_op = First(operand="$items")
        assert first_op.expression == {"$first": "$items"}
