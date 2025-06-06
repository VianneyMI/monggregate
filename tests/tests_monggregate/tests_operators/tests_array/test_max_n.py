"""Tests for `monggregate.operators.array.max_n` module."""

from monggregate.operators.array.max_n import MaxN


class TestMaxN:
    """Tests for `MaxN` class."""

    def test_instantiation(self) -> None:
        """Test that `MaxN` class can be instantiated."""
        max_n_op = MaxN(input=[1, 2, 3], n=2)
        assert isinstance(max_n_op, MaxN)

    def test_expression(self) -> None:
        """Test that `MaxN` class returns the correct expression."""
        max_n_op = MaxN(input=[1, 2, 3], n=2)
        assert max_n_op.expression == {"$maxN": {"input": [1, 2, 3], "n": 2}}
