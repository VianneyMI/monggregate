import pytest
from monggregate.fields import FieldName, FieldPath, Variable


class TestFieldName:
    """Test the FieldName class."""

    def test_validate_valid_field_name(self):
        """Test that a valid field name passes validation."""
        # Setup
        field_name = "validField"

        # Act
        result = FieldName.validate(field_name)

        # Assert
        assert result == field_name

    def test_validate_invalid_field_name_with_dollar(self):
        """Test that a field name starting with $ fails validation."""
        # Setup
        field_name = "$invalidField"

        # Act & Assert
        with pytest.raises(ValueError):
            FieldName.validate(field_name)

    def test_validate_invalid_field_name_with_dot(self):
        """Test that a field name containing a dot fails validation."""
        # Setup
        field_name = "invalid.field"

        # Act & Assert
        with pytest.raises(ValueError):
            FieldName.validate(field_name)

    def test_validate_edge_case_empty_string(self):
        """Test that an empty string fails validation."""
        # Setup
        field_name = ""

        # Act & Assert
        with pytest.raises(ValueError):
            FieldName.validate(field_name)


class TestFieldPath:
    """Test the FieldPath class."""

    def test_validate_valid_field_path(self) -> None:
        """Test that a valid field path passes validation."""
        # Setup
        field_path = "$validPath"

        # Act
        result = FieldPath.validate(field_path)

        # Assert
        assert result == field_path

    def test_validate_invalid_field_path_without_dollar(self) -> None:
        """Test that a field path without $ fails validation."""
        # Setup
        field_path = "invalidPath"

        # Act & Assert
        with pytest.raises(ValueError):
            FieldPath.validate(field_path)

    # @pytest.mark.xfail(reason="Should be fixed in the code.")
    def test_validate_invalid_field_path_with_double_dollar(self) -> None:
        """Test that a field path with $$ fails validation."""
        # Setup
        field_path = "$$invalidPath"

        # Act & Assert
        with pytest.raises(ValueError):
            FieldPath.validate(field_path)

    pytest.mark.xfail(
        reason="This passes but should fail. Need to be fixed in the code"
    )

    def test_validate_edge_case_single_dollar(self) -> None:
        """Test that just a single $ passes validation."""
        # Setup
        field_path = "$"

        # Act
        result = FieldPath.validate(field_path)

        # Assert
        assert result == field_path


class TestVariable:
    """Test the Variable class."""

    def test_validate_valid_variable(self) -> None:
        """Test that a valid variable passes validation."""
        # Setup
        variable = "$$validVariable"

        # Act
        result = Variable.validate(variable)

        # Assert
        assert result == variable

    def test_validate_invalid_variable_without_dollars(self) -> None:
        """Test that a variable without $$ fails validation."""
        # Setup
        variable = "invalidVariable"

        # Act & Assert
        with pytest.raises(ValueError):
            Variable.validate(variable)

    def test_validate_invalid_variable_with_single_dollar(self) -> None:
        """Test that a variable with single $ fails validation."""
        # Setup
        variable = "$invalidVariable"

        # Act & Assert
        with pytest.raises(ValueError):
            Variable.validate(variable)

    def test_validate_edge_case_system_variable(self) -> None:
        """Test that a system variable passes validation."""
        # Setup
        variable = "$$NOW"

        # Act
        result = Variable.validate(variable)

        # Assert
        assert result == variable


def test_field_types_validation() -> None:
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
