import pytest
from monggregate.operators.operator import Operator


def test_operator_instantiation():
    """Test that Operator base class can be instantiated correctly."""

    # Create a simple subclass of Operator for testing
    class TestOperator(Operator):
        name = "testOp"

        def _validate(self):
            pass

    # Instantiate the operator with a simple operand
    test_op = TestOperator(operand="value")

    # Check that the expression is correctly formatted
    assert test_op.expression == {"$testOp": "value"}

    # Test with a complex operand
    complex_op = TestOperator(operand={"field": "$amount", "limit": 10})
    assert complex_op.expression == {"$testOp": {"field": "$amount", "limit": 10}}
