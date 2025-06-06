"""Tests for `monggregate.operators.objects.merge_objects` module."""

from monggregate.operators.objects.merge_objects import MergeObjects

def test_merge_objects_expression():
    # Setup
    operand = [{"field1": 1}, {"field2": 2}]
    expected_expression = {"$mergeObjects": operand}

    # Act
    merge_objects_op = MergeObjects(operand=operand)
    result_expression = merge_objects_op.expression

    # Assert
    assert result_expression == expected_expression


class TestMergeObjects:
    """Tests for `MergeObjects` class."""

    def test_instantiation_with_single_operand(self) -> None:
        """Test that `MergeObjects` class can be instantiated with a single operand."""
        merge_objects_op = MergeObjects(operand={"field1": 1, "field2": 2})
        assert isinstance(merge_objects_op, MergeObjects)

    def test_instantiation_with_multiple_operands(self) -> None:
        """Test that `MergeObjects` class can be instantiated with multiple operands."""
        merge_objects_op = MergeObjects(operand=[{"field1": 1}, {"field2": 2}])
        assert isinstance(merge_objects_op, MergeObjects)

    def test_expression_with_single_operand(self) -> None:
        """Test that `MergeObjects` class returns the correct expression with a single operand."""
        merge_objects_op = MergeObjects(operand={"field1": 1, "field2": 2})
        assert merge_objects_op.expression == {
            "$mergeObjects": {"field1": 1, "field2": 2}
        }

    def test_expression_with_multiple_operands(self) -> None:
        """Test that `MergeObjects` class returns the correct expression with multiple operands."""
        merge_objects_op = MergeObjects(operand=[{"field1": 1}, {"field2": 2}])
        assert merge_objects_op.expression == {
            "$mergeObjects": [{"field1": 1}, {"field2": 2}]
        }
