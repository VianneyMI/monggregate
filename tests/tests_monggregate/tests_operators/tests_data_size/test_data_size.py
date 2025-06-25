"""Tests for `monggregate.operators.data_size.data_size` module."""

import pytest

from monggregate.operators.data_size.data_size import (
    DataSizeOperator,
    DataSizeOperatorEnum,
)
from tests.utils import generate_enum_member_name


class TestDataSizeOperator:
    """Tests for the `DataSizeOperator` class."""

    def test_is_abstract(self) -> None:
        """Test that `DataSizeOperator` is an abstract class."""
        with pytest.raises(TypeError):
            DataSizeOperator()


class TestDataSizeOperatorEnum:
    """Tests for the `DataSizeOperatorEnum` class."""

    def test_naming_convention(self) -> None:
        """Test that the naming convention is correct."""
        mismatches = []

        for member in DataSizeOperatorEnum:
            expected_name = generate_enum_member_name(member.value)
            if member.name != expected_name:
                mismatches.append(
                    f"\n- {member.name}: got '{member.name}', expected '{expected_name}'"
                )

        assert not mismatches, (
            "The following members do not follow the naming convention:"
            f"{''.join(mismatches)}"
        )
