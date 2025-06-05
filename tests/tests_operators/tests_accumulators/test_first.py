import pytest
from monggregate.operators.accumulators.first import First, first

def test_first_expression():
    #Setup
    operand = "$someField"
    expected_expression = {
        "$first": operand
    }

    #Act
    first_op = first(operand)
    result_expression = first_op.expression

    #Assert
    assert result_expression == expected_expression