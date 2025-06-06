"""Tests for `monggregate.operators.conditional.if_null` module."""

from monggregate.operators.conditional.if_null import IfNull


class TestIfNull:
    """Tests for `IfNull` class."""

    def test_instantiation(self) -> None:
        """Test that `IfNull` class can be instantiated."""
        if_null_op = IfNull(operand="$optional_field", output="default_value")
        assert isinstance(if_null_op, IfNull)

    def test_expression(self) -> None:
        """Test that `IfNull` class returns the correct expression."""
        if_null_op = IfNull(operand="$optional_field", output="default_value")
        assert if_null_op.expression == {
            "$ifNull": ["$optional_field", "default_value"]
        }
