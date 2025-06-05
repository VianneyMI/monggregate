import pytest
from monggregate.operators.accumulators.count import Count, count

def test_count_expression():
    # Setup
    expected_expression = {
        "$count": {}
    }

    # Act
    count_op = count()            
    result_expression = count_op.expression

    # Assert
    assert result_expression == expected_expression