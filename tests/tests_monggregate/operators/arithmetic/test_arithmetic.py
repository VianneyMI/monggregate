import pytest
from monggregate.operators.arithmetic.arithmetic import (
    ArithmeticOperator,
    ArithmeticOperatorEnum,
)


def test_arithmetic_operator_enum():
    """Test that ArithmeticOperatorEnum contains the expected values."""
    # Check a few of the enum values
    assert ArithmeticOperatorEnum.ADD == "$add"
    assert ArithmeticOperatorEnum.SUBTRACT == "$subtract"
    assert ArithmeticOperatorEnum.MULTIPLY == "$multiply"
    assert ArithmeticOperatorEnum.DIVIDE == "$divide"
    assert ArithmeticOperatorEnum.POW == "$pow"

    # Test string conversion
    assert str(ArithmeticOperatorEnum.ADD) == "$add"
    assert str(ArithmeticOperatorEnum.MULTIPLY) == "$multiply"


def test_arithmetic_operator_inheritance():
    """Test that ArithmeticOperator is properly defined as an abstract base class."""

    # Create a simple implementation of ArithmeticOperator for testing
    class TestArithmeticOperator(ArithmeticOperator):
        name = "testArithmetic"
        operands = [1, 2]

        def _validate(self):
            pass

    # Instantiate the test operator
    test_op = TestArithmeticOperator()

    # Check that it's an instance of ArithmeticOperator
    assert isinstance(test_op, ArithmeticOperator)
