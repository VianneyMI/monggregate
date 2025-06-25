"""Tests for `monggregate.operators.conditional.conditional` module."""

import pytest

from monggregate.operators.conditional.conditional import (
    ConditionalOperator,
    ConditionalOperatorEnum,
)
from tests.utils import generate_enum_member_name


class TestConditionalOperator:
    """Tests for the `ConditionalOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `ConditionalOperator` is an abstract class."""
        with pytest.raises(TypeError):
            ConditionalOperator()


class TestConditionalOperatorEnum:
    """Tests for the `ConditionalOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in ConditionalOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
