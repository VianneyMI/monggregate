import pytest
from monggregate.operators.accumulators.push import Push, push

def test_push_expression():
    #Setup
    operand = "$someField"
    expected_expression = {
        "$push": operand
    }

    #Act
    push_op = push(operand)
    result_expression = push_op.expression

    #Assert
    assert result_expression == expected_expression