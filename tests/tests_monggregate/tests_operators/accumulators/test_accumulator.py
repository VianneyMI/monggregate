import pytest
from monggregate.operators.accumulators.accumulator import Accumulator, AccumulatorEnum


def test_accumulator_enum():
    """Test that AccumulatorEnum contains the expected values."""
    # Check a few of the enum values
    assert AccumulatorEnum.AVG == "$avg"
    assert AccumulatorEnum.SUM == "$sum"
    assert AccumulatorEnum.COUNT == "$count"
    assert AccumulatorEnum.FIRST == "$first"
    assert AccumulatorEnum.LAST == "$last"
    assert AccumulatorEnum.MAX == "$max"
    assert AccumulatorEnum.MIN == "$min"
    assert AccumulatorEnum.PUSH == "$push"

    # Test string conversion
    assert str(AccumulatorEnum.AVG) == "$avg"
    assert str(AccumulatorEnum.SUM) == "$sum"


def test_accumulator_inheritance():
    """Test that Accumulator is properly defined as an abstract base class."""

    # Create a simple implementation of Accumulator for testing
    class TestAccumulator(Accumulator):
        name = "testAccumulator"
        operand = None

        def _validate(self):
            pass

    # Instantiate the test accumulator
    test_acc = TestAccumulator()

    # Check that it's an instance of Accumulator
    assert isinstance(test_acc, Accumulator)
