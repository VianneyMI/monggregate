"""Tests for `monggregate.operators.array.filter` module."""

from monggregate.operators.array.filter import Filter


class TestFilter:
    """Tests for `Filter` class."""

    def test_instantiation(self) -> None:
        """Test that `Filter` class can be instantiated."""
        filter_op = Filter(operand="$items", query={"$gt": ["$$num", 5]}, let="num")
        assert isinstance(filter_op, Filter)

    def test_expression(self) -> None:
        """Test that `Filter` class returns the correct expression."""
        filter_op = Filter(
            operand="$items", query={"$gt": ["$$num", 5]}, let="num", limit=3
        )
        assert filter_op.expression == {
            "$filter": {
                "input": "$items",
                "cond": {"$gt": ["$$num", 5]},
                "as": "num",
                "limit": 3,
            }
        }
