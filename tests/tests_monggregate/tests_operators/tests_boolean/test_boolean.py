"""Tests for `monggregate.operators.boolean.boolean` module."""

import pytest

from monggregate.operators.boolean.boolean import BooleanOperator, BooleanOperatorEnum
from tests.utils import generate_enum_member_name


class TestBooleanOperator:
    """Tests for the `BooleanOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `BooleanOperator` is an abstract class."""
        with pytest.raises(TypeError):
            BooleanOperator()


class TestBooleanOperatorEnum:
    """Tests for the `BooleanOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in BooleanOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
