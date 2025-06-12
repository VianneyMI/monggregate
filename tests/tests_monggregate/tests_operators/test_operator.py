"""Tests for `monggregate.operators.operator` module."""

import pytest

from monggregate.operators.operator import Operator, OperatorEnum


def generate_enum_member_name(value: str) -> str:
    """Generate the expected enum member name from a value.

    Args:
        value: The enum value (with or without $ prefix)

    Returns:
        The expected member name in UPPER_SNAKE_CASE format

    Example:
        >>> generate_enum_member_name("$addToSet")
        'ADD_TO_SET'
        >>> generate_enum_member_name("bottomN")
        'BOTTOM_N'
    """
    # Remove the $ prefix if present
    value_name = value[1:] if value.startswith("$") else value

    # Split camelCase into words
    words = []
    current_word = value_name[0]

    for char in value_name[1:]:
        if char.isupper():
            words.append(current_word)
            current_word = char
        else:
            current_word += char

    words.append(current_word)

    # Convert to UPPER_SNAKE_CASE
    return "_".join(word.upper() for word in words)


class TestOperator:
    """Tests for the `Operator` class."""

    def test_is_abstract(self) -> None:
        """Test that `Operator` is an abstract class."""
        with pytest.raises(TypeError):
            Operator()


class TestOperatorEnum:
    """Tests for the `OperatorEnum` class."""

    @pytest.mark.xfail(
        reason="""Some operators are not following the naming convention.
        Ex: INDEX_OF_CP
        
        Need to review the generate_enum_member_name function.
        """
    )
    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in OperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
