"""Tests for `monggregate.search.commons.fuzzy` module."""

import pytest

from monggregate.search.commons.fuzzy import FuzzyOptions


class TestFuzzyOptions:
    """Tests for the `FuzzyOptions` class."""

    def test_default_values(self) -> None:
        """Test that `FuzzyOptions` has the correct default values."""
        options = FuzzyOptions()
        assert options.max_edits == 2
        assert options.max_expansions == 50
        assert options.prefix_length == 0

    def test_custom_values(self) -> None:
        """Test that `FuzzyOptions` accepts custom values."""
        options = FuzzyOptions(max_edits=1, max_expansions=100, prefix_length=2)
        assert options.max_edits == 1
        assert options.max_expansions == 100
        assert options.prefix_length == 2

    def test_expression_property(self) -> None:
        """Test that `FuzzyOptions` has an expression property."""
        options = FuzzyOptions()
        expression = options.expression
        assert expression is not None

    def test_alias_mapping(self) -> None:
        """Test that `FuzzyOptions` fields are properly aliased."""
        options = FuzzyOptions()
        data = options.dict(by_alias=True)
        assert "maxEdits" in data
        assert "maxExpansions" in data
        assert "prefixLength" in data
