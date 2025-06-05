"""Tests for `monggregate.operators.strings.concat` module."""

from monggregate.operators.strings.concat import Concat


class TestConcat:
    """Tests for `Concat` class."""

    def test_instantiation(self) -> None:
        """Test that `Concat` class can be instantiated."""
        concat_op = Concat(operands=["$firstName", " ", "$lastName"])
        assert isinstance(concat_op, Concat)

    def test_expression(self) -> None:
        """Test that `Concat` class returns the correct expression."""
        concat_op = Concat(operands=["$firstName", " ", "$lastName"])
        assert concat_op.expression == {"$concat": ["$firstName", " ", "$lastName"]}
