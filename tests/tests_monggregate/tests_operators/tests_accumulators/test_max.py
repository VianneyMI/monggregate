"""Tests for `monggregate.operators.accumulators.max` module."""

import pytest
from monggregate.operators.accumulators.max import Max, max

def test_max_expression():
    # Setup
    operand = "$someNumericField"
    expected_expression = {
        "$max": operand
    }

    # Act
    max_op = max(operand)
    result_expression = max_op.expression

    # Assert
    assert result_expression == expected_expression


class TestMax:
    """Tests for `Max` class."""

    def test_instantiation(self) -> None:
        """Test that `Max` class can be instantiated."""
        max_op = Max(operand=1)
        assert isinstance(max_op, Max)

    def test_expression(self) -> None:
        """Test that `Max` class returns the correct expression."""
        max_op = Max(operand=1)
        assert max_op.expression == {"$max": 1}