"""Tests for `monggregate.operators.accumulators.last` module."""

import pytest
from monggregate.operators.accumulators.last import Last, last

def test_last_expression():
    # Setup
    operand = "$someField"
    expected_expression = {
        "$last": operand
    }

    # Act
    last_op = last(operand)
    result_expression = last_op.expression

    # Assert
    assert result_expression == expected_expression


class TestLast:
    """Tests for `Last` class."""

    def test_instantiation(self) -> None:
        """Test that `Last` class can be instantiated."""
        last_op = Last(operand=1)
        assert isinstance(last_op, Last)

    def test_expression(self) -> None:
        """Test that `Last` class returns the correct expression."""
        last_op = Last(operand=1)
        assert last_op.expression == {"$last": 1}