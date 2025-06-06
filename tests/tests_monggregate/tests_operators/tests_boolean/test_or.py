"""Tests for `monggregate.operators.boolean.or_` module."""

from monggregate.operators.boolean.or_ import Or


class TestOr:
    """Tests for `Or` class."""

    def test_instantiation(self) -> None:
        """Test that `Or` class can be instantiated."""
        or_op = Or(operands=[{"$eq": ["$status", "active"]}, {"$gt": ["$priority", 5]}])
        assert isinstance(or_op, Or)

    def test_expression(self) -> None:
        """Test that `Or` class returns the correct expression."""
        or_op = Or(operands=[{"$eq": ["$status", "active"]}, {"$gt": ["$priority", 5]}])
        assert or_op.expression == {
            "$or": [{"$eq": ["$status", "active"]}, {"$gt": ["$priority", 5]}]
        }
