import pytest
from monggregate.stages import Match


class TestMatch:
    """Tests for the Match stage."""

    def test_instantiation(self) -> None:
        """Test that the Match stage can be instantiated correctly with a simple query."""
        match = Match(query={"status": "active"})
        assert isinstance(match, Match)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        match = Match(query={"status": "active"})
        assert match.expression == {"$match": {"status": "active"}}

    def test_expression_with_expr(self) -> None:
        """Test that the expression method returns the correct expression."""

        match = Match(expr={"field": {"$gt": 10}})

        # When using MQL operator, we should use the "expr" attribute so that
        # the expression is correctly formatted by inserting the "$expr" operator.

        # fmt: off
        assert match.expression == {
            "$match": {
                "$expr": {
                    "field": {"$gt": 10}
                    }
                }
        }
        # fmt: on
