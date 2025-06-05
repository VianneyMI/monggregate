"""Tests for `monggregate.operators.accumulators.accumulator` module."""

import pytest

from monggregate.operators.accumulators.accumulator import Accumulator, AccumulatorEnum


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


class TestAccumulator:
    """Tests for the `Accumulator` class."""

    def test_is_abstract(self) -> None:
        """Test that `Accumulator` is an abstract class."""

        with pytest.raises(TypeError):
            Accumulator()


class TestAccumulatorEnum:
    """Tests for the `AccumulatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in AccumulatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
