"""Tests for the BucketAuto stage."""

from monggregate.stages import BucketAuto
from monggregate.stages.bucket_auto import GranularityEnum


class TestBucketAuto:
    """Tests for the BucketAuto stage."""

    def test_instantiation(self) -> None:
        """Test that the BucketAuto stage can be instantiated."""
        stage = BucketAuto(
            group_by="field",
            buckets=10,
        )
        assert isinstance(stage, BucketAuto)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        stage = BucketAuto(group_by="field", buckets=10)
        # fmt: off
        assert stage.expression == {
            "$bucketAuto": {
                "groupBy": "$field",
                "buckets": 10,
                "output": None,
                "granularity": None,
                }
        }
        # fmt: on

    def test_with_output(self) -> None:
        """Test that the output parameter is validated."""

        stage = BucketAuto(group_by="field", buckets=10, output={"count": {"$sum": 1}})
        assert stage.expression == {
            "$bucketAuto": {
                "groupBy": "$field",
                "buckets": 10,
                "output": {"count": {"$sum": 1}},
                "granularity": None,
            }
        }

    def test_with_granularity(self) -> None:
        """Test that the granularity parameter is validated."""

        stage = BucketAuto(group_by="field", buckets=10, granularity="R10")

        # Check that the granularity is stored as an instance of GranularityEnum
        assert isinstance(stage.granularity, GranularityEnum)

        # fmt: off
        assert stage.expression == {
            "$bucketAuto": {
                "groupBy": "$field",
                "buckets": 10,
                "output": None,
                "granularity": "R10", # Granularity gets serialized correctly
                                      # When passing to expression
                }
        }
        # fmt: on
