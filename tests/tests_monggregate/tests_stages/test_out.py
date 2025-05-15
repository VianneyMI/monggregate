"""Tests for the Out stage."""

import pytest
from monggregate.stages import Out


class TestOut:
    """Tests for the Out stage."""

    def test_instantiation(self) -> None:
        """Test that the Out stage can be instantiated correctly."""
        out = Out(collection="test_collection")
        assert isinstance(out, Out)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        out = Out(collection="test_collection")
        assert out.expression == {"$out": "test_collection"}

    def test_expression_with_db(self) -> None:
        """Test that the expression method returns the correct expression with a database."""

        out = Out(collection="test_collection", db="test_db")
        assert out.expression == {"$out": {"db": "test_db", "coll": "test_collection"}}
