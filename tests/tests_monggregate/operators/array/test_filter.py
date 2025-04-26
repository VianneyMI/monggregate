import pytest
from monggregate.operators.array.filter import Filter, filter


def test_filter_instantiation():
    """Test that Filter class can be instantiated correctly."""
    # Test with basic configuration
    filter_operator = Filter(
        operand="$items", query={"$gt": ["$$this.price", 100]}, let="this", limit=None
    )

    expected_expression = {
        "$filter": {
            "input": "$items",
            "cond": {"$gt": ["$$this.price", 100]},
            "as": "this",
            "limit": None,
        }
    }

    assert filter_operator.expression == expected_expression

    # Test with custom variable name and limit
    filter_operator2 = Filter(
        operand="$products",
        query={"$eq": ["$$item.category", "electronics"]},
        let="item",
        limit=5,
    )

    expected_expression2 = {
        "$filter": {
            "input": "$products",
            "cond": {"$eq": ["$$item.category", "electronics"]},
            "as": "item",
            "limit": 5,
        }
    }

    assert filter_operator2.expression == expected_expression2


def test_filter_factory_function():
    """Test that the filter factory function works correctly."""
    # Test with all parameters
    filter_op = filter(
        operand="$scores", let="score", query={"$gte": ["$$score", 70]}, limit=10
    )

    expected_expression = {
        "$filter": {
            "input": "$scores",
            "cond": {"$gte": ["$$score", 70]},
            "as": "score",
            "limit": 10,
        }
    }

    assert filter_op.expression == expected_expression

    # Test without limit
    filter_op2 = filter(
        operand="$tags", let="tag", query={"$in": ["$$tag", ["important", "urgent"]]}
    )

    expected_expression2 = {
        "$filter": {
            "input": "$tags",
            "cond": {"$in": ["$$tag", ["important", "urgent"]]},
            "as": "tag",
            "limit": None,
        }
    }

    assert filter_op2.expression == expected_expression2
