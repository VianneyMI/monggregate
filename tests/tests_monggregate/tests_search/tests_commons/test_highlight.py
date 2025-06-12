"""Tests for `monggregate.search.commons.highlight` module."""

import pytest

from monggregate.search.commons.highlight import (
    HighlightOptions,
    HighlightText,
    HightlightOutput,
)


class TestHighlightOptions:
    """Tests for the `HighlightOptions` class."""

    def test_required_fields(self) -> None:
        """Test that `HighlightOptions` has the required fields."""
        options = HighlightOptions(path="field")
        assert options.path == "field"

    def test_default_values(self) -> None:
        """Test that `HighlightOptions` has the correct default values."""
        options = HighlightOptions(path="field")
        assert options.max_chars_to_examine == 500000
        assert options.max_num_passages == 5

    def test_custom_values(self) -> None:
        """Test that `HighlightOptions` accepts custom values."""
        options = HighlightOptions(
            path="field", max_chars_to_examine=100000, max_num_passages=3
        )
        assert options.path == "field"
        assert options.max_chars_to_examine == 100000
        assert options.max_num_passages == 3

    def test_alias_mapping(self) -> None:
        """Test that `HighlightOptions` fields are properly aliased."""
        options = HighlightOptions(path="field")
        data = options.dict(by_alias=True)
        assert "maxCharsToExamine" in data
        assert "maxNumPassages" in data


class TestHighlightText:
    """Tests for the `HighlightText` class."""

    def test_required_fields(self) -> None:
        """Test that `HighlightText` has the required fields."""
        text = HighlightText(value="test", type="hit")
        assert text.value == "test"
        assert text.type == "hit"

    def test_type_validation(self) -> None:
        """Test that `HighlightText` validates the type field."""
        with pytest.raises(ValueError):
            HighlightText(value="test", type="invalid")


class TestHighlightOutput:
    """Tests for the `HighlightOutput` class."""

    def test_required_fields(self) -> None:
        """Test that `HighlightOutput` has the required fields."""
        output = HightlightOutput(
            path="field", texts=[HighlightText(value="test", type="hit")], score=1.0
        )
        assert output.path == "field"
        assert len(output.texts) == 1
        assert output.score == 1.0
