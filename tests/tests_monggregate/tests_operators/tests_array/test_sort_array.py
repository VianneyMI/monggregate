"""Tests for `monggregate.operators.array.sort_array` module."""

from monggregate.operators.array.sort_array import SortArray


class TestSortArray:
    """Tests for `SortArray` class."""

    def test_instantiation(self) -> None:
        """Test that `SortArray` class can be instantiated."""
        sort_array_op = SortArray(operand=[3, 1, 2], sort_by=1)
        assert isinstance(sort_array_op, SortArray)

    def test_expression(self) -> None:
        """Test that `SortArray` class returns the correct expression."""
        sort_array_op = SortArray(operand=[3, 1, 2], sort_by=1)
        assert sort_array_op.expression == {
            "$sortArray": {"input": [3, 1, 2], "sortBy": 1}
        }
