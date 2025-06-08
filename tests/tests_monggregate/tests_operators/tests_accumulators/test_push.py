"""Tests for `monggregate.operators.accumulators.push` module."""

import pytest
from monggregate.operators.accumulators.push import Push, push

def test_push_expression():
    # Setup
    operand = "$someField"
    expected_expression = {
        "$push": operand
    }

    # Act
    push_op = push(operand)
    result_expression = push_op.expression

    # Assert
    assert result_expression == expected_expression


class TestPush:
    """Tests for `Push` class."""

    def test_instantiation(self) -> None:
        """Test that `Push` class can be instantiated."""
        push_op = Push(operand=1)
        assert isinstance(push_op, Push)

    def test_expression(self) -> None:
        """Test that `Push` class returns the correct expression."""
        push_op = Push(operand=1)
        assert push_op.expression == {"$push": 1}