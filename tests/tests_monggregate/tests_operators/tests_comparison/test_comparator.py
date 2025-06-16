"""Tests for `monggregate.operators.comparison.comparator` module."""

import pytest

from monggregate.operators.comparison.comparator import Comparator, ComparatorEnum
from tests.utils import generate_enum_member_name


class TestComparator:
    """Tests for the `Comparator` class."""

    def test_is_abstract(self) -> None:
        """Test that `Comparator` is an abstract class."""
        with pytest.raises(TypeError):
            Comparator()


class TestComparatorEnum:
    """Tests for the `ComparatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in ComparatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
