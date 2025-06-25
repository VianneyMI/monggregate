"""Tests for `monggregate.operators.arithmetic.arithmetic` module."""

import pytest

from monggregate.operators.arithmetic.arithmetic import (
    ArithmeticOperator,
    ArithmeticOperatorEnum,
)
from tests.utils import generate_enum_member_name


class TestArithmeticOperator:
    """Tests for the `ArithmeticOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `ArithmeticOperator` is an abstract class."""
        with pytest.raises(TypeError):
            ArithmeticOperator()


class TestArithmeticOperatorEnum:
    """Tests for the `ArithmeticOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in ArithmeticOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
