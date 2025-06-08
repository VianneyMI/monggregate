"""Tests for `monggregate.operators.array.filter` module."""

from monggregate.operators.array.filter import Filter

def test_filter_expression():
    # Setup
    operand = [1, 2, 3, 4, 5]
    let = "num"
    query = {"$gt": ["$$num", 5]}
    limit = None
    expected_expression = {
        "$filter": {
            "input": operand,
            "cond": query,
            "as": let,
            "limit": limit
        }
    }

    # Act
    filter_op = Filter(operand=operand, query=query, let=let, limit=limit)
    result_expression = filter_op.expression

    # Assert
    assert result_expression == expected_expression


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
