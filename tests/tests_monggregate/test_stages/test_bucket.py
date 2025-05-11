"""Tests for the Bucket stage."""

import pytest
from monggregate.stages import Bucket


class TestBucket:
    """Tests for the Bucket stage."""

    def test_instantiation(self) -> None:
        """Test that Bucket stage can be instantiated correctly."""
        # Test with basic configuration
        bucket_stage = Bucket(by="$price", boundaries=[0, 100, 200, 300, 400])
        assert isinstance(bucket_stage, Bucket)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        bucket_stage = Bucket(by="$price", boundaries=[0, 100, 200, 300, 400])
        # fmt: off
        expected_expression = {
            "$bucket": {
                "groupBy": "$price",
                "boundaries": [0, 100, 200, 300, 400],
                "default": None,
                "output": None,
            }
        }

        assert bucket_stage.expression == expected_expression

    def test_with_default(self) -> None:
        """Test that the default parameter is validated."""

        # Test with default value
        bucket_stage = Bucket(
            by="$age", boundaries=[20, 30, 40, 50, 60, 70], default="other"
        )

        expected_expression = {
            "$bucket": {
                "groupBy": "$age",
                "boundaries": [20, 30, 40, 50, 60, 70],
                "default": "other",
                "output": None,
            }
        }

        assert bucket_stage.expression == expected_expression

    def test_with_custom_output(self) -> None:
        """Test that the output parameter is validated."""

        # Test with custom output
        bucket_stage = Bucket(
            by="$score",
            boundaries=[0, 50, 70, 90, 100],
            default="outlier",
            output={"count": {"$sum": 1}, "avg_score": {"$avg": "$score"}},
        )

        expected_expression = {
            "$bucket": {
                "groupBy": "$score",
                "boundaries": [0, 50, 70, 90, 100],
                "default": "outlier",
                "output": {"count": {"$sum": 1}, "avg_score": {"$avg": "$score"}},
            }
        }

        assert bucket_stage.expression == expected_expression
