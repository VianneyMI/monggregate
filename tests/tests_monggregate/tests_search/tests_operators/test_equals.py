import pytest
from monggregate.search.operators.equals import Equals

def test_equals_expression():
    # Setup
    path = "status"
    value = True
    score = {"boost": 3}

    equals_op = Equals(path=path, value=value, score=score)

    expected_expression = {
        "equals": {
            "path": path,
            "value": value,
            "score": score
        }
    }

    # Act
    actual_expression = equals_op.expression

    # Assert
    assert actual_expression == expected_expression
