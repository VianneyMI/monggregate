"""Tests for `monggregate.operators.comparison.gt` module."""

from monggregate.operators.comparison.gt import GreatherThan


class TestGreatherThan:
    """Tests for `GreatherThan` class."""

    def test_instantiation(self) -> None:
        """Test that `GreatherThan` class can be instantiated."""
        gt_op = GreatherThan(left="$field", right=10)
        assert isinstance(gt_op, GreatherThan)

    def test_expression(self) -> None:
        """Test that `GreatherThan` class returns the correct expression."""
        gt_op = GreatherThan(left="$field", right=10)
        assert gt_op.expression == {"$gt": ["$field", 10]}
