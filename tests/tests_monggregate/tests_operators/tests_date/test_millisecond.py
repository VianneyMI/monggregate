"""Tests for `monggregate.operators.date.millisecond` module."""

from monggregate.operators.date.millisecond import Millisecond

def test_millisecond_expression():
    # Setup
    operand = "$date"
    timezone = "America/New_York"
    expected_expression = {
        "$millisecond": {"date": operand, "timezone": timezone}
    }

    # Act
    millisecond_op = Millisecond(operand=operand, timezone=timezone)
    result_expression = millisecond_op.expression

    # Assert
    assert result_expression == expected_expression



class TestMillisecond:
    """Tests for `Millisecond` class."""

    def test_instantiation(self) -> None:
        """Test that `Millisecond` class can be instantiated."""
        millisecond_op = Millisecond(operand="$date", timezone=None)
        assert isinstance(millisecond_op, Millisecond)

    def test_expression_without_timezone(self) -> None:
        """Test that `Millisecond` class returns the correct expression without timezone."""
        millisecond_op = Millisecond(operand="$date", timezone=None)
        assert millisecond_op.expression == {"$millisecond": "$date"}

    def test_expression_with_timezone(self) -> None:
        """Test that `Millisecond` class returns the correct expression with timezone."""
        millisecond_op = Millisecond(operand="$date", timezone="America/New_York")
        assert millisecond_op.expression == {
            "$millisecond": {"date": "$date", "timezone": "America/New_York"}
        }
