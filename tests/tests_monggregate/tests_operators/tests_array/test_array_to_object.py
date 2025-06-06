"""Tests for `monggregate.operators.array.array_to_object` module."""

from monggregate.operators.array.array_to_object import ArrayToObject

def test_array_to_object_expression():
    # Setup
    operand = [ { "k": "item", "v": "abc123"}, { "k": "qty", "v": 25 } ]
    expected_expression = { "$arrayToObject": operand }

    # Act
    array_to_object_op = ArrayToObject(operand=operand)
    result_expression = array_to_object_op.expression

    # Assert
    assert result_expression == expected_expression


class TestArrayToObject:
    """Tests for `ArrayToObject` class."""

    def test_instantiation(self) -> None:
        """Test that `ArrayToObject` class can be instantiated."""
        array_to_object_op = ArrayToObject(operand=[["item", "abc123"], ["qty", 25]])
        assert isinstance(array_to_object_op, ArrayToObject)

    def test_expression(self) -> None:
        """Test that `ArrayToObject` class returns the correct expression."""
        array_to_object_op = ArrayToObject(operand=[["item", "abc123"], ["qty", 25]])
        assert array_to_object_op.expression == {
            "$arrayToObject": [["item", "abc123"], ["qty", 25]]
        }