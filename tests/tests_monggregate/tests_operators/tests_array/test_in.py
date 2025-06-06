"""Tests for `monggregate.operators.array.in_` module."""

from monggregate.operators.array.in_ import In


class TestIn:
    """Tests for `In` class."""

    def test_instantiation(self) -> None:
        """Test that `In` class can be instantiated."""
        in_op = In(left="$value", right=["$array"])
        assert isinstance(in_op, In)

    def test_expression(self) -> None:
        """Test that `In` class returns the correct expression."""
        in_op = In(left="$value", right=["$array"])
        assert in_op.expression == {"$in": ["$value", ["$array"]]}
