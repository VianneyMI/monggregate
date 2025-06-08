"""Tests for `monggregate.operators.comparison.gte` module."""

from monggregate.operators.comparison.gte import GreatherThanOrEqual

from monggregate.operators.comparison.gte import GreatherThanOrEqual

def test_greather_than_or_equal_expression():
    # Setup
    left = "$field"
    right = 10
    expected_expression = {"$gte": [left, right]}

    # Act
    gte_op = GreatherThanOrEqual(left=left, right=right)
    result_expression = gte_op.expression

    # Assert
    assert result_expression == expected_expression


class TestGreatherThanOrEqual:
    """Tests for `GreatherThanOrEqual` class."""

    def test_instantiation(self) -> None:
        """Test that `GreatherThanOrEqual` class can be instantiated."""
        gte_op = GreatherThanOrEqual(left="$field", right=10)
        assert isinstance(gte_op, GreatherThanOrEqual)

    def test_expression(self) -> None:
        """Test that `GreatherThanOrEqual` class returns the correct expression."""
        gte_op = GreatherThanOrEqual(left="$field", right=10)
        assert gte_op.expression == {"$gte": ["$field", 10]}
