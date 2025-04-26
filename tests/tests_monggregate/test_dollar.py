import pytest
from monggregate.dollar import Dollar, DollarDollar


def test_dollar_instantiation():
    """Test that Dollar class can be accessed correctly and returns dollar-prefixed fields."""
    # Test field reference
    assert Dollar.name == "$name"

    # Test field() method
    assert Dollar().field("price") == "$price"

    # Test operator method (e.g. sum)
    sum_op = Dollar.sum("$amount")
    assert sum_op.expression == {"$sum": "$amount"}
