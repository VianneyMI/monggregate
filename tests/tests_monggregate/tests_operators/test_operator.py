"""Tests for `monggregate.operators.operator` module."""

import pytest

from monggregate.operators.operator import Operator, OperatorEnum
from tests.utils import generate_enum_member_name


class TestOperator:
    """Tests for the `Operator` class."""

    def test_is_abstract(self) -> None:
        """Test that `Operator` is an abstract class."""
        with pytest.raises(TypeError):
            Operator()


class TestOperatorEnum:
    """Tests for the `OperatorEnum` class."""

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
