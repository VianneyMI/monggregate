"""Tests for the SortByCount stage."""

import pytest
from monggregate.stages import SortByCount


class TestSortByCount:
    """Tests for the SortByCount stage."""

    def test_instantiation(self) -> None:
        """Test that the SortByCount stage can be instantiated correctly."""

        sort_by_count = SortByCount(by="field1")
        assert isinstance(sort_by_count, SortByCount)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        sort_by_count = SortByCount(by="field1")
        assert sort_by_count.expression == {"$sortByCount": "$field1"}

    def test_expression_with_other_types(self) -> None:
        """Test that the expression method returns the correct expression with other types."""

        sort_by_count = SortByCount(by=["field1", "field2"])
        assert sort_by_count.expression == {"$sortByCount": {"$field1", "$field2"}}
