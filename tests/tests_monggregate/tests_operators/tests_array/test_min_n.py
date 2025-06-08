"""Tests for `monggregate.operators.array.min_n` module."""

from monggregate.operators.array.min_n import MinN

def test_minn_expression():
    # Setup
    operand = [3, 1, 4, 1, 5]
    limit = 2
    expected_expression = {
        "$minN": {
            "n": limit,
            "input": operand
        }
    }

    # Act
    min_n_op = MinN(operand=operand, limit=limit)
    result_expression = min_n_op.expression

    # Assert
    assert result_expression == expected_expression


class TestMinN:
    """Tests for `MinN` class."""

    def test_instantiation(self) -> None:
        """Test that `MinN` class can be instantiated."""
        min_n_op = MinN(operand=[3, 1, 4, 1, 5], limit=2)
        assert isinstance(min_n_op, MinN)

    def test_expression(self) -> None:
        """Test that `MinN` class returns the correct expression."""
        min_n_op = MinN(operand=[3, 1, 4, 1, 5], limit=2)
        assert min_n_op.expression == {"$minN": {"n": 2, "input": [3, 1, 4, 1, 5]}}