"""Tests for `monggregate.operators.comparison.ne` module."""

from monggregate.operators.comparison.ne import NotEqual

def test_not_equal_expression():
    # Setup
    left = "$field"
    right = 10
    expected_expression = {"$ne": [left, right]}

    # Act
    ne_op = NotEqual(left=left, right=right)
    result_expression = ne_op.expression

    # Assert
    assert result_expression == expected_expression


class TestNotEqual:
    """Tests for `NotEqual` class."""

    def test_instantiation(self) -> None:
        """Test that `NotEqual` class can be instantiated."""
        not_equal_op = NotEqual(left="$field", right=10)
        assert isinstance(not_equal_op, NotEqual)

    def test_expression(self) -> None:
        """Test that `NotEqual` class returns the correct expression."""
        not_equal_op = NotEqual(left="$field", right=10)
        assert not_equal_op.expression == {"$ne": ["$field", 10]}
