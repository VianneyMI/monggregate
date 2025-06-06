"""Tests for `monggregate.operators.array.last` module."""

from monggregate.operators.array.last import Last

from monggregate.operators.array.is_array import IsArray

def test_is_array_expression():
    # Setup
    operand = [1, 2, 3]
    expected_expression = {"$isArray": operand}

    # Act
    is_array_op = IsArray(operand=operand)
    result_expression = is_array_op.expression

    # Assert
    assert result_expression == expected_expression


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
