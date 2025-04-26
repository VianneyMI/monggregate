import pytest
from monggregate.fields import FieldName, FieldPath, Variable


def test_field_types_validation():
    """Test that field types validate input correctly."""
    # Valid field name (no $ at start, no dots)
    assert FieldName.validate("validField") == "validField"

    # Valid field path (starts with $)
    assert FieldPath.validate("$validPath") == "$validPath"

    # Valid variable (starts with $$)
    assert Variable.validate("$$validVariable") == "$$validVariable"

    # Invalid field name (starts with $)
    with pytest.raises(ValueError):
        FieldName.validate("$invalidField")

    # Invalid field name (contains dot)
    with pytest.raises(ValueError):
        FieldName.validate("invalid.field")
