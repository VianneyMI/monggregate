import pytest
from monggregate.operators.accumulators.min import Min, min

def test_min_expression():
    #Setup
    operand = "$someNumericField"
    expected_expression = {
        "$min": operand
    }

    #Act
    min_op = min(operand)
    result_expression = min_op.expression

    #Assert
    assert result_expression == expected_expression