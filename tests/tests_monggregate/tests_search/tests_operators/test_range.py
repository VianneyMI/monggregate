import pytest
from datetime import datetime
from monggregate.search.operators.range import Range

def test_range_expression_with_numeric_bounds():
    # Setup
    range_op = Range(
        path="price",
        gt=10,
        lte=100,
        score={"boost": 2}
    )
    expected = {
        "range": {
            "path": "price",
            "gt": 10,
            "lte": 100,
            "score": {"boost": 2}
        }
    }

    # Act
    expression = range_op.expression

    # Assert
    
    assert expression == expected