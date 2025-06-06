"""Tests for `monggregate.operators.accumulators.avg` module."""

from monggregate.operators.accumulators.avg import Average, avg

def test_avg_expression():
    # Setup
    expected_expression = {
        "$avg": None
    }

    # Act
    avg_op = Average()            
    result_expression = avg_op.expression

    # Assert
    assert result_expression == expected_expression

class TestAverage:
    """Tests for `Average` class."""

    def test_instantiation(self) -> None:
        """Test that `Average` class can be instantiated."""
        average = Average(operand=1)
        assert isinstance(average, Average)

    def test_expression(self) -> None:
        """Test that `Average` class returns the correct expression."""

        average = Average(operand=1)
        assert average.expression == {"$avg": 1}