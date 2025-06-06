"""Tests for `monggregate.operators.array.is_array` module."""

from monggregate.operators.array.is_array import IsArray


class TestIsArray:
    """Tests for `IsArray` class."""

    def test_instantiation(self) -> None:
        """Test that `IsArray` class can be instantiated."""
        is_array_op = IsArray(operand="$field")
        assert isinstance(is_array_op, IsArray)

    def test_expression(self) -> None:
        """Test that `IsArray` class returns the correct expression."""
        is_array_op = IsArray(operand="$field")
        assert is_array_op.expression == {"$isArray": "$field"}
