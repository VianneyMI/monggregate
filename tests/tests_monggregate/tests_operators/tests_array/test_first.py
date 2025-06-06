"""Tests for `monggregate.operators.array.first` module."""

from monggregate.operators.array.first import First

from monggregate.operators.array.first import First

def test_first_expression():
    # Setup
    array = [10, 20, 30]
    expected_expression = {"$first": array}

    # Act
    first_op = First(operand=array)
    result_expression = first_op.expression

    # Assert
    assert result_expression == expected_expression


class TestFirst:
    """Tests for `First` class."""

    def test_instantiation(self) -> None:
        """Test that `First` class can be instantiated."""
        first_op = First(operand="$items")
        assert isinstance(first_op, First)

    def test_expression(self) -> None:
        """Test that `First` class returns the correct expression."""
        first_op = First(operand="$items")
        assert first_op.expression == {"$first": "$items"}
