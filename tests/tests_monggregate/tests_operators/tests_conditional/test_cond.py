"""Tests for `monggregate.operators.conditional.cond` module."""

from monggregate.operators.conditional.cond import Cond


class TestCond:
    """Tests for `Cond` class."""

    def test_instantiation_with_if_then_else(self) -> None:
        """Test that `Cond` class can be instantiated with if/then/else syntax."""
        cond_op = Cond(if_={"$gt": ["$age", 18]}, then_="Adult", else_="Minor")
        assert isinstance(cond_op, Cond)

    def test_expression_with_if_then_else(self) -> None:
        """Test that `Cond` class returns the correct expression with if/then/else syntax."""
        cond_op = Cond(if_={"$gt": ["$age", 18]}, then_="Adult", else_="Minor")
        assert cond_op.expression == {
            "$cond": {"if": {"$gt": ["$age", 18]}, "then": "Adult", "else": "Minor"}
        }
