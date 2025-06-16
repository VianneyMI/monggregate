"""Tests for `monggregate.operators.date.date` module."""

import pytest

from monggregate.operators.date.date import DateOperator, DateOperatorEnum
from tests.utils import generate_enum_member_name


class TestDateOperator:
    """Tests for the `DateOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `DateOperator` is an abstract class."""
        with pytest.raises(TypeError):
            DateOperator()


class TestDateOperatorEnum:
    """Tests for the `DateOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in DateOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
