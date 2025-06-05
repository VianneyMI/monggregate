import pytest
from monggregate.operators.accumulators.last import Last, last

def test_last_expression():
    #Setup
    operand = "$someField"
    expected_expression = {
        "$last": operand
    }

    #Act
    last_op = last(operand)
    result_expression = last_op.expression

    #Assert
    assert result_expression == expected_expression