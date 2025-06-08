"""Tests for `monggregate.operators.objects.object_to_array` module."""

from monggregate.operators.objects.object_to_array import ObjectToArray

def test_object_to_array_expression():
    # Setup
    operand = "$document"
    expected_expression = {"$objectToArray": "$document"}

    # Act
    object_to_array_op = ObjectToArray(operand=operand)
    result_expression = object_to_array_op.expression

    # Assert
    assert result_expression == expected_expression


class TestObjectToArray:
    """Tests for `ObjectToArray` class."""

    def test_instantiation(self) -> None:
        """Test that `ObjectToArray` class can be instantiated."""
        object_to_array_op = ObjectToArray(operand="$document")
        assert isinstance(object_to_array_op, ObjectToArray)

    def test_expression(self) -> None:
        """Test that `ObjectToArray` class returns the correct expression."""
        object_to_array_op = ObjectToArray(operand="$document")
        assert object_to_array_op.expression == {"$objectToArray": "$document"}
