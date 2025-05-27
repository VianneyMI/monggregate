"""Tests for the Unset stage."""

import pytest
from monggregate.stages import Unset


class TestUnset:
    """Tests for the Unset stage."""

    def test_instantiation(self) -> None:
        """Test that the Unset stage can be instantiated."""

        unset = Unset(field="field")
        assert isinstance(unset, Unset)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        unset = Unset(field="field")
        assert unset.expression == {"$unset": "field"}

    def test_expression_with_fields(self) -> None:
        """Test that the expression method returns the correct expression with fields."""

        unset = Unset(fields=["field1", "field2"])
        assert unset.expression == {"$unset": ["field1", "field2"]}
