import pytest
from monggregate.operators.accumulators.sum import Sum, sum


def test_sum_instantiation():
    """Test that Sum class can be instantiated correctly."""
    # Test with a field reference
    sum_operator = Sum(operand="$price")
    assert sum_operator.expression == {"$sum": "$price"}

    # Test with a numeric value
    sum_operator2 = Sum(operand=1)
    assert sum_operator2.expression == {"$sum": 1}

    # Test with a more complex expression
    sum_operator3 = Sum(operand={"$multiply": ["$price", "$quantity"]})
    assert sum_operator3.expression == {"$sum": {"$multiply": ["$price", "$quantity"]}}

    # Test with an array of values
    sum_operator4 = Sum(operand=["$price", "$tax", "$shipping"])
    assert sum_operator4.expression == {"$sum": ["$price", "$tax", "$shipping"]}


def test_sum_factory_function():
    """Test that the sum factory function works correctly."""
    # Test with a single argument
    sum_op1 = sum("$revenue")
    assert sum_op1.expression == {"$sum": "$revenue"}

    # Test with multiple arguments
    sum_op2 = sum("$price", "$tax", "$shipping")
    assert sum_op2.expression == {"$sum": ["$price", "$tax", "$shipping"]}

    # Verify it returns the correct type
    assert isinstance(sum_op1, Sum)
    assert isinstance(sum_op2, Sum)
