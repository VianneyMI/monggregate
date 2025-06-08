"""Tests for `monggregate.operators.array.sort_array` module."""

from monggregate.operators.array.sort_array import SortArray

def test_sort_array_expression():
    # Setup
    array = [{"score": 10}, {"score": 20}, {"score": 30}]
    sort_by = {"score": 1}
    expected_expression = {
        "$sortArray": {
            "input": array,
            "sortBy": sort_by
        }
    }

    # Act
    sort_op = SortArray(operand=array, by=sort_by)
    result_expression = sort_op.expression

    # Assert
    assert result_expression == expected_expression


class TestSortArray:
    """Tests for `SortArray` class."""

    def test_instantiation(self) -> None:
        """Test that `SortArray` class can be instantiated."""
        sort_array_op = SortArray(operand="$items", by={"score": 1})
        assert isinstance(sort_array_op, SortArray)

    def test_expression(self) -> None:
        """Test that `SortArray` class returns the correct expression."""
        sort_array_op = SortArray(operand="$items", by={"score": 1})
        assert sort_array_op.expression == {
            "$sortArray": {"input": "$items", "sortBy": {"score": 1}}
        }
