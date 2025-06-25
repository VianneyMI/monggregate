"""Tests for `monggregate.operators.array.array` module."""

import pytest

from monggregate.operators.array.array import ArrayOperator, ArrayOperatorEnum
from tests.utils import generate_enum_member_name


class TestArrayOperator:
    """Tests for the `ArrayOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `ArrayOperator` is an abstract class."""
        with pytest.raises(TypeError):
            ArrayOperator()


class TestArrayOperatorEnum:
    """Tests for the `ArrayOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in ArrayOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
