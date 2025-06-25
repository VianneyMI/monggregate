"""Tests for `monggregate.operators.accumulators.accumulator` module."""

import pytest

from monggregate.operators.accumulators.accumulator import Accumulator, AccumulatorEnum
from tests.utils import generate_enum_member_name


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
