import pytest
from monggregate.search.operators.compound import Compound

def test_compound_expression_with_must_equals():
    # Setup
    compound = Compound()
    path = "field"
    value = "test"
    compound.equals("must", path=path, value=value)

    expected_expression = {
        "compound": {
            "must": [
                {
                    "equals": {
                        "path": path,
                        "value": value
                    }
                }
            ]
        }
    }

    # Act
    actual_expression = compound.expression

    # Assert
    assert actual_expression == expected_expression