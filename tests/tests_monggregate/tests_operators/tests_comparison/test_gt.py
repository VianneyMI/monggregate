"""Tests for `monggregate.operators.comparison.gt` module."""

from monggregate.operators.comparison.gt import GreatherThan

def test_greather_than_expression():
    # Setup
    left = "$field"
    right = 10
    expected_expression = {"$gt": [left, right]}

    # Act
    gt_op = GreatherThan(left=left, right=right)
    result_expression = gt_op.expression

    # Assert
    assert result_expression == expected_expression


class TestGreatherThan:
    """Tests for `GreatherThan` class."""

    def test_instantiation(self) -> None:
        """Test that `GreatherThan` class can be instantiated."""
        gt_op = GreatherThan(left="$field", right=10)
        assert isinstance(gt_op, GreatherThan)

    def test_expression(self) -> None:
        """Test that `GreatherThan` class returns the correct expression."""
        gt_op = GreatherThan(left="$field", right=10)
        assert gt_op.expression == {"$gt": ["$field", 10]}
        
