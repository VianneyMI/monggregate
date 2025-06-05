"""Tests for `monggregate.operators.comparison.ne` module."""

from monggregate.operators.comparison.ne import NotEqual


class TestNotEqual:
    """Tests for `NotEqual` class."""

    def test_instantiation(self) -> None:
        """Test that `NotEqual` class can be instantiated."""
        not_equal_op = NotEqual(left="$field", right=10)
        assert isinstance(not_equal_op, NotEqual)

    def test_expression(self) -> None:
        """Test that `NotEqual` class returns the correct expression."""
        not_equal_op = NotEqual(left="$field", right=10)
        assert not_equal_op.expression == {"$ne": ["$field", 10]}
