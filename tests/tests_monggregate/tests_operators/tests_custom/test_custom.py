"""Tests for `monggregate.operators.custom.custom` module."""

import pytest

from monggregate.operators.custom.custom import CustomOperator, CustomOperatorEnum
from tests.utils import generate_enum_member_name


class TestCustomOperator:
    """Tests for the `CustomOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `CustomOperator` is an abstract class."""
        with pytest.raises(TypeError):
            CustomOperator()


class TestCustomOperatorEnum:
    """Tests for the `CustomOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in CustomOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
