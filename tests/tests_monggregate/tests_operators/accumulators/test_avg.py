import pytest
from monggregate.operators.accumulators.avg import Average, Avg, average, avg


def test_average_instantiation():
    """Test that Average class can be instantiated correctly."""
    # Test with a field reference
    avg_operator = Average(operand="$price")
    assert avg_operator.expression == {"$avg": "$price"}

    # Test with a numeric value
    avg_operator2 = Average(operand=10)
    assert avg_operator2.expression == {"$avg": 10}

    # Test with a more complex expression
    avg_operator3 = Average(operand={"$multiply": ["$price", "$quantity"]})
    assert avg_operator3.expression == {"$avg": {"$multiply": ["$price", "$quantity"]}}


def test_avg_alias():
    """Test that Avg is an alias for Average."""
    assert Avg is Average

    avg_op = Avg(operand="$value")
    assert avg_op.expression == {"$avg": "$value"}


def test_factory_functions():
    """Test that the factory functions work correctly."""
    # Test the average function
    avg_op1 = average(operand="$price")
    assert avg_op1.expression == {"$avg": "$price"}

    # Test the avg alias function
    avg_op2 = avg(operand="$quantity")
    assert avg_op2.expression == {"$avg": "$quantity"}

    # Verify they return the correct type
    assert isinstance(avg_op1, Average)
    assert isinstance(avg_op2, Average)
