"""Tests for `monggregate.operators.comparison.lt` module."""

from monggregate.operators.comparison.lt import LowerThan

def test_lower_than_expression():
    # Setup
    left = "$field"
    right = 10
    expected_expression = {"$lt": [left, right]}

    # Act
    lt_op = LowerThan(left=left, right=right)
    result_expression = lt_op.expression

    # Assert
    assert result_expression == expected_expression


class TestLowerThan:
    """Tests for `LowerThan` class."""

    def test_instantiation(self) -> None:
        """Test that `LowerThan` class can be instantiated."""
        lt_op = LowerThan(left="$field", right=10)
        assert isinstance(lt_op, LowerThan)

    def test_expression(self) -> None:
        """Test that `LowerThan` class returns the correct expression."""
        lt_op = LowerThan(left="$field", right=10)
        assert lt_op.expression == {"$lt": ["$field", 10]}
