"""Tests for `monggregate.operators.strings.string` module."""

import pytest

from monggregate.operators.strings.string import StringOperator, StringOperatorEnum
from tests.utils import generate_enum_member_name


class TestStringOperator:
    """Tests for the `StringOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `StringOperator` is an abstract class."""
        with pytest.raises(TypeError):
            StringOperator()


class TestStringOperatorEnum:
    """Tests for the `StringOperatorEnum` class."""

    @pytest.mark.xfail(
        reason="""Some operators are not following the naming convention.
        Ex: CONCAT_WS
        
        Need to review the generate_enum_member_name function.
        """
    )
    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in StringOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
