"""Tests for `monggregate.operators.comparison.lte` module."""

from monggregate.operators.comparison.lte import LowerThanOrEqual

def test_lower_than_or_equal_expression():
    # Setup
    left = "$field"
    right = 10
    expected_expression = {"$lte": [left, right]}

    # Act
    lte_op = LowerThanOrEqual(left=left, right=right)
    result_expression = lte_op.expression

    # Assert
    assert result_expression == expected_expression


class TestLowerThanOrEqual:
    """Tests for `LowerThanOrEqual` class."""

    def test_instantiation(self) -> None:
        """Test that `LowerThanOrEqual` class can be instantiated."""
        lte_op = LowerThanOrEqual(left="$field", right=10)
        assert isinstance(lte_op, LowerThanOrEqual)

    def test_expression(self) -> None:
        """Test that `LowerThanOrEqual` class returns the correct expression."""
        lte_op = LowerThanOrEqual(left="$field", right=10)
        assert lte_op.expression == {"$lte": ["$field", 10]}
