"""Tests for `monggregate.operators.array.min_n` module."""

from monggregate.operators.array.min_n import MinN


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
