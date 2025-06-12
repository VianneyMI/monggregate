"""Tests for `monggregate.search.commons.count` module."""

import pytest

from monggregate.search.commons.count import CountOptions, CountResults


class TestCountOptions:
    """Tests for the `CountOptions` class."""

    def test_default_values(self) -> None:
        """Test that `CountOptions` has the correct default values."""
        options = CountOptions()
        assert options.type == "lowerBound"
        assert options.threshold == 1000

    def test_custom_values(self) -> None:
        """Test that `CountOptions` accepts custom values."""
        options = CountOptions(type="total", threshold=500)
        assert options.type == "total"
        assert options.threshold == 500

    def test_type_validation(self) -> None:
        """Test that `CountOptions` validates the type field."""
        options = CountOptions(type="lower_bound")
        assert options.type == "lowerBound"

    def test_expression_property(self) -> None:
        """Test that `CountOptions` has an expression property."""
        options = CountOptions()
        expression = options.expression
        assert expression is not None


class TestCountResults:
    """Tests for the `CountResults` class."""

    def test_has_required_fields(self) -> None:
        """Test that `CountResults` has the required fields."""
        results = CountResults(lower_bound=10, total=20)
        assert results.lower_bound == 10
        assert results.total == 20

    def test_optional_fields(self) -> None:
        """Test that `CountResults` fields are optional."""
        results = CountResults()
        assert results.lower_bound is None
        assert results.total is None

    def test_expression_property(self) -> None:
        """Test that `CountResults` has an expression property."""
        results = CountResults(lower_bound=10, total=20)
        expression = results.expression
        assert expression is not None
