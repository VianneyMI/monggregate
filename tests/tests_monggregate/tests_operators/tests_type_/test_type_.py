"""Tests for `monggregate.operators.type_.type_` module."""

from monggregate.operators.type_.type_ import Type_

def test_type_expression():
    # Setup
    operand = "$field"
    expected_expression = {"$type": "$field"}

    # Act
    type_op = Type_(operand=operand)
    result_expression = type_op.expression

    # Assert
    assert result_expression == expected_expression


class TestType:
    """Tests for `Type_` class."""

    def test_instantiation(self) -> None:
        """Test that `Type_` class can be instantiated."""
        type_op = Type_(operand="$field")
        assert isinstance(type_op, Type_)

    def test_expression(self) -> None:
        """Test that `Type_` class returns the correct expression."""
        type_op = Type_(operand="$field")
        assert type_op.expression == {"$type": "$field"}
