"""Tests for `monggregate.operators.comparison.eq` module."""

from monggregate.operators.comparison.eq import Equal

def test_equal_expression():
    # Setup
    left = "$field"
    right = 10
    expected_expression = {"$eq": [left, right]}

    # Act
    equal_op = Equal(left=left, right=right)
    result_expression = equal_op.expression

    # Assert
    assert result_expression == expected_expression


class TestEqual:
    """Tests for `Equal` class."""

    def test_instantiation(self) -> None:
        """Test that `Equal` class can be instantiated."""
        equal_op = Equal(left="$field", right=10)
        assert isinstance(equal_op, Equal)

    def test_expression(self) -> None:
        """Test that `Equal` class returns the correct expression."""
        equal_op = Equal(left="$field", right=10)
        assert equal_op.expression == {"$eq": ["$field", 10]}
