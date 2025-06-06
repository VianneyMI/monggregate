"""Tests for `monggregate.operators.accumulators.first` module."""

import pytest
from monggregate.operators.accumulators.first import First, first

def test_first_expression():
    # Setup
    operand = "$someField"
    expected_expression = {
        "$first": operand
    }

    # Act
    first_op = first(operand)
    result_expression = first_op.expression

    # Assert
    assert result_expression == expected_expression


class TestFirst:
    """Tests for `First` class."""

    def test_instantiation(self) -> None:
        """Test that `First` class can be instantiated."""
        first_op = First(operand=1)
        assert isinstance(first_op, First)

    def test_expression(self) -> None:
        """Test that `First` class returns the correct expression."""
        first_op = First(operand=1)
        assert first_op.expression == {"$first": 1}