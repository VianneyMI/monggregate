"""Tests for `monggregate.operators.conditional.switch` module."""

from monggregate.operators.conditional.switch import Switch

def test_switch_expression():
    # Setup
    branches = [
        {"case": {"$eq": ["$grade", "A"]}, "then": "Type A"},
        {"case": {"$eq": ["$grade", "B"]}, "then": "Type B"},
    ]
    default = "Unknown Type"
    expected_expression = {
        "$switch": {
            "branches": branches,
            "default": default
        }
    }

    # Act
    switch_op = Switch(branches=branches, default=default)
    result_expression = switch_op.expression

    # Assert
    assert result_expression == expected_expression


class TestSwitch:
    """Tests for `Switch` class."""

    def test_instantiation(self) -> None:
        """Test that `Switch` class can be instantiated."""
        switch_op = Switch(
            branches=[
                {"case": {"$eq": ["$type", "A"]}, "then": "Type A"},
                {"case": {"$eq": ["$type", "B"]}, "then": "Type B"},
            ],
            default="Unknown Type",
        )
        assert isinstance(switch_op, Switch)

    def test_expression(self) -> None:
        """Test that `Switch` class returns the correct expression."""
        switch_op = Switch(
            branches=[
                {"case": {"$eq": ["$type", "A"]}, "then": "Type A"},
                {"case": {"$eq": ["$type", "B"]}, "then": "Type B"},
            ],
            default="Unknown Type",
        )
        assert switch_op.expression == {
            "$switch": {
                "branches": [
                    {"case": {"$eq": ["$type", "A"]}, "then": "Type A"},
                    {"case": {"$eq": ["$type", "B"]}, "then": "Type B"},
                ],
                "default": "Unknown Type",
            }
        }
