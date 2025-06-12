"""Tests for `monggregate.search.collectors.facet` module."""

import pytest

from monggregate.search.collectors.facet import Facet, FacetName, FacetBucket


class TestFacetName:
    """Tests for the `FacetName` class."""

    def test_is_subclass_of_field_name(self) -> None:
        """Test that `FacetName` is a subclass of `FieldName`."""
        from monggregate.fields import FieldName

        assert issubclass(FacetName, FieldName)


class TestFacetBucket:
    """Tests for the `FacetBucket` class."""

    @pytest.mark.xfail(
        reason="Pydantic v1 ignore fields starting with _. Will be fixed in Pydantic v2 or by config."
    )
    def test_has_required_fields(self) -> None:
        """Test that `FacetBucket` has the required fields."""
        bucket = FacetBucket(_id="test", count=1)
        assert bucket._id == "test"
        assert bucket.count == 1


class TestFacet:
    """Tests for the `Facet` class."""

    def test_is_subclass_of_search_collector(self) -> None:
        """Test that `Facet` is a subclass of `SearchCollector`."""
        from monggregate.search.collectors.collector import SearchCollector

        assert issubclass(Facet, SearchCollector)

    def test_init_autocomplete(self) -> None:
        """Test that `init_autocomplete` creates a facet with an autocomplete operator."""
        from monggregate.search.operators import Autocomplete

        facet = Facet.init_autocomplete(query="test", path="field")
        assert isinstance(facet.operator, Autocomplete)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"

    def test_init_text(self) -> None:
        """Test that `init_text` creates a facet with a text operator."""
        from monggregate.search.operators import Text

        facet = Facet.init_text(query="test", path="field")
        assert isinstance(facet.operator, Text)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"

    def test_init_regex(self) -> None:
        """Test that `init_regex` creates a facet with a regex operator."""
        from monggregate.search.operators import Regex

        facet = Facet.init_regex(query="test", path="field")
        assert isinstance(facet.operator, Regex)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"

    def test_init_wildcard(self) -> None:
        """Test that `init_wildcard` creates a facet with a wildcard operator."""
        from monggregate.search.operators import Wildcard

        facet = Facet.init_wildcard(query="test", path="field")
        assert isinstance(facet.operator, Wildcard)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"
