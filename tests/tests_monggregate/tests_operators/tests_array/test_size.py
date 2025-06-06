"""Tests for `monggregate.operators.array.size` module."""

from monggregate.operators.array.size import Size

def test_size_expression():
    # Setup
    array = ["a", "b", "c"]
    expected_expression = {"$size": array}

    # Act
    size_op = Size(operand=array)
    result_expression = size_op.expression

    # Assert
    assert result_expression == expected_expression


class TestSize:
    """Tests for `Size` class."""

    def test_instantiation(self) -> None:
        """Test that `Size` class can be instantiated."""
        size_op = Size(operand="$items")
        assert isinstance(size_op, Size)

    def test_expression(self) -> None:
        """Test that `Size` class returns the correct expression."""
        size_op = Size(operand="$items")
        assert size_op.expression == {"$size": "$items"}
