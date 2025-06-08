"""Tests for `monggregate.operators.accumulators.min` module."""

import pytest
from monggregate.operators.accumulators.min import Min, min

def test_min_expression():
    # Setup
    operand = "$someNumericField"
    expected_expression = {
        "$min": operand
    }

    # Act
    min_op = min(operand)
    result_expression = min_op.expression

    # Assert
    assert result_expression == expected_expression


class TestMin:
    """Tests for `Min` class."""

    def test_instantiation(self) -> None:
        """Test that `Min` class can be instantiated."""
        min_op = Min(operand=1)
        assert isinstance(min_op, Min)

    def test_expression(self) -> None:
        """Test that `Min` class returns the correct expression."""
        min_op = Min(operand=1)
        assert min_op.expression == {"$min": 1}