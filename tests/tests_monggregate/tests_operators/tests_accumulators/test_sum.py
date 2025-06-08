"""Tests for `monggregate.operators.accumulators.sum` module."""

import pytest
from monggregate.operators.accumulators.sum import Sum, sum

def test_sum_operand():
    # Setup
    operand = "$amount"

    # Act
    result_op = {"$sum": operand}
    expected_expression = {"$sum": "$amount"}

    # Assert
    assert result_op == expected_expression


class TestSum:
    """Tests for `Sum` class."""

    def test_instantiation(self) -> None:
        """Test that `Sum` class can be instantiated."""
        sum_op = Sum(operand=1)
        assert isinstance(sum_op, Sum)

    def test_expression(self) -> None:
        """Test that `Sum` class returns the correct expression."""
        sum_op = Sum(operand=1)
        assert sum_op.expression == {"$sum": 1}