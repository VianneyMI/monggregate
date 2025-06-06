"""Tests for `monggregate.operators.array.last` module."""

from monggregate.operators.array.last import Last


class TestLast:
    """Tests for `Last` class."""

    def test_instantiation(self) -> None:
        """Test that `Last` class can be instantiated."""
        last_op = Last(operand="$items")
        assert isinstance(last_op, Last)

    def test_expression(self) -> None:
        """Test that `Last` class returns the correct expression."""
        last_op = Last(operand="$items")
        assert last_op.expression == {"$last": "$items"}
