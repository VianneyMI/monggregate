"""Tests for the UnionWith stage."""

import pytest
from monggregate.stages import UnionWith


class TestUnionWith:
    """Tests for the UnionWith stage."""

    def test_instantiation(self) -> None:
        """Test that the UnionWith stage can be instantiated."""

        union_with = UnionWith(collection="test_collection")
        assert isinstance(union_with, UnionWith)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        union_with = UnionWith(collection="test_collection")
        assert union_with.expression == {"$unionWith": "test_collection"}

    def test_expression_with_pipeline(self) -> None:
        """Test that the expression method returns the correct expression with a pipeline."""

        union_with = UnionWith(
            collection="test_collection", pipeline=[{"$match": {"field": "value"}}]
        )
        assert union_with.expression == {
            "$unionWith": {
                "coll": "test_collection",
                "pipeline": [{"$match": {"field": "value"}}],
            }
        }
