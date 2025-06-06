"""Tests for `monggregate.operators.boolean.not_` module."""

from monggregate.operators.boolean.not_ import Not


class TestNot:
    """Tests for `Not` class."""

    def test_instantiation(self) -> None:
        """Test that `Not` class can be instantiated."""
        not_op = Not(operand={"$eq": ["$status", "inactive"]})
        assert isinstance(not_op, Not)

    def test_expression(self) -> None:
        """Test that `Not` class returns the correct expression."""
        not_op = Not(operand={"$eq": ["$status", "inactive"]})
        assert not_op.expression == {"$not": [{"$eq": ["$status", "inactive"]}]}
