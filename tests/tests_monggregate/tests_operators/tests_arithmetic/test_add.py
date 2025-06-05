"""Tests for `monggregate.operators.arithmetic.add` module."""

from monggregate.operators.arithmetic.add import Add


class TestAdd:
    """Tests for `Add` class."""

    def test_instantiation(self) -> None:
        """Test that `Add` class can be instantiated."""
        add_op = Add(operands=[1, 2, 3])
        assert isinstance(add_op, Add)

    def test_expression(self) -> None:
        """Test that `Add` class returns the correct expression."""
        add_op = Add(operands=[1, 2, 3])
        assert add_op.expression == {"$add": [1, 2, 3]}
