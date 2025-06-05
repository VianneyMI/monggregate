"""Tests for `monggregate.operators.accumulators.push` module."""

from monggregate.operators.accumulators.push import Push


class TestPush:
    """Tests for `Push` class."""

    def test_instantiation(self) -> None:
        """Test that `Push` class can be instantiated."""
        push_op = Push(operand=1)
        assert isinstance(push_op, Push)

    def test_expression(self) -> None:
        """Test that `Push` class returns the correct expression."""
        push_op = Push(operand=1)
        assert push_op.expression == {"$push": 1}
