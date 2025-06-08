"""Tests for `monggregate.operators.boolean.and_` module."""

from monggregate.operators.boolean.and_ import And

def test_and_expression():
    # Setup
    expressions = [{"$gt": 18}, {"$lt": 65}]
    expected_expression = {"$and": expressions}

    # Act
    and_op = And(operands=expressions)
    result_expression = and_op.expression

    # Assert
    assert result_expression == expected_expression


class TestAnd:
    """Tests for `And` class."""

    def test_instantiation(self) -> None:
        """Test that `And` class can be instantiated."""
        and_op = And(operands=[{"$gt": ["$age", 18]}, {"$lt": ["$age", 65]}])
        assert isinstance(and_op, And)

    def test_expression(self) -> None:
        """Test that `And` class returns the correct expression."""
        and_op = And(operands=[{"$gt": ["$age", 18]}, {"$lt": ["$age", 65]}])
        assert and_op.expression == {
            "$and": [{"$gt": ["$age", 18]}, {"$lt": ["$age", 65]}]
        }
