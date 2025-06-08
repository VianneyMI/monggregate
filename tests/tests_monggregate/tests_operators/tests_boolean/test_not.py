"""Tests for `monggregate.operators.boolean.not_` module."""

from monggregate.operators.boolean.not_ import Not

def test_not_expression():
    # Setup
    operand = {"$eq": ["inactive"]}
    expected_expression = {"$not": [operand]}

    # Act
    not_op = Not(operand=operand)
    result_expression = not_op.expression

    # Assert
    assert result_expression == expected_expression


class TestNot:
    """Tests for `Not` class."""

    def test_instantiation(self) -> None:
        """Test that `Not` class can be instantiated."""
        not_op = Not(operand={"$eq": ["$status", "inactive"]})
        assert isinstance(not_op, Not)

    def test_expression(self) -> None:
        """Test that `Not` class returns the correct expression."""
        not_op = Not(operand={"$eq": ["$status", "inactive"]})
        assert not_op.expression == {"$not": [{"$eq": ["$status", "inactive"]}]}
