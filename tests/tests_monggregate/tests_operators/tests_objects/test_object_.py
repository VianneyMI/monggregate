"""Tests for `monggregate.operators.objects.object_` module."""

import pytest

from monggregate.operators.objects.object_ import ObjectOperator, ObjectOperatorEnum
from tests.utils import generate_enum_member_name


class TestObjectOperator:
    """Tests for the `ObjectOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `ObjectOperator` is an abstract class."""
        with pytest.raises(TypeError):
            ObjectOperator()


class TestObjectOperatorEnum:
    """Tests for the `ObjectOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in ObjectOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
