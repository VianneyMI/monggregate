import pytest
from monggregate.utils import (
    to_unique_list,
    validate_field_path,
    validate_field_paths,
    StrEnum,
)


def test_to_unique_list():
    """Test that to_unique_list converts inputs to a list of unique values."""
    # Test with a string
    assert to_unique_list("field") == ["field"]

    # Test with a list (with duplicates)
    assert sorted(to_unique_list(["field1", "field2", "field1"])) == [
        "field1",
        "field2",
    ]

    # Test with a set
    assert sorted(to_unique_list({"field1", "field2"})) == ["field1", "field2"]

    # Test with non-convertible type
    non_convertible = {"key": "value"}
    assert to_unique_list(non_convertible) is non_convertible


def test_validate_field_path():
    """Test that validate_field_path adds $ prefix to paths when needed."""
    # Path without $ prefix
    assert validate_field_path("field") == "$field"

    # Path already with $ prefix
    assert validate_field_path("$field") == "$field"

    # None value
    assert validate_field_path(None) is None
