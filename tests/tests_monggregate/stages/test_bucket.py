import pytest
from monggregate.stages import Bucket


def test_bucket_instantiation():
    """Test that Bucket stage can be instantiated correctly."""
    # Test with basic configuration
    bucket_stage = Bucket(by="$price", boundaries=[0, 100, 200, 300, 400])

    expected_expression = {
        "$bucket": {
            "groupBy": "$price",
            "boundaries": [0, 100, 200, 300, 400],
            "default": None,
            "output": None,
        }
    }

    assert bucket_stage.expression == expected_expression

    # Test with default value
    bucket_stage2 = Bucket(
        by="$age", boundaries=[20, 30, 40, 50, 60, 70], default="other"
    )

    expected_expression2 = {
        "$bucket": {
            "groupBy": "$age",
            "boundaries": [20, 30, 40, 50, 60, 70],
            "default": "other",
            "output": None,
        }
    }

    assert bucket_stage2.expression == expected_expression2

    # Test with custom output
    bucket_stage3 = Bucket(
        by="$score",
        boundaries=[0, 50, 70, 90, 100],
        default="outlier",
        output={"count": {"$sum": 1}, "avg_score": {"$avg": "$score"}},
    )

    expected_expression3 = {
        "$bucket": {
            "groupBy": "$score",
            "boundaries": [0, 50, 70, 90, 100],
            "default": "outlier",
            "output": {"count": {"$sum": 1}, "avg_score": {"$avg": "$score"}},
        }
    }

    assert bucket_stage3.expression == expected_expression3
