import pytest
from monggregate.operators.accumulators.max import Max, max

def test_max_expression():
    #Setup
    operand = "$someNumericField"
    expected_expression = {
        "$max": operand
    }

    #Act
    max_op = max(operand)
    result_expression = max_op.expression

    #Assert
    assert result_expression == expected_expression