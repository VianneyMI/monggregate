"""Tests for `monggregate.operators.arithmetic.add` module."""

from monggregate.operators.arithmetic.add import Add

def test_add_expression():
    # Setup
    operands = [1, 2, 3]
    expected_expression = {"$add": operands}

    # Act
    add_op = Add(operands=operands)
    result_expression = add_op.expression

    # Assert
    assert result_expression == expected_expression


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
