import pytest
from monggregate.operators.arithmetic.add import Add, add


def test_add_instantiation():
    """Test that Add class can be instantiated correctly."""
    # Test with two numeric values
    add_operator = Add(operands=[5, 10])
    assert add_operator.expression == {"$add": [5, 10]}

    # Test with field references
    add_operator2 = Add(operands=["$price", "$tax"])
    assert add_operator2.expression == {"$add": ["$price", "$tax"]}

    # Test with a mix of fields and values
    add_operator3 = Add(operands=["$basePrice", 10, "$tax"])
    assert add_operator3.expression == {"$add": ["$basePrice", 10, "$tax"]}

    # Test with nested expressions
    add_operator4 = Add(operands=["$price", {"$multiply": ["$quantity", "$unitPrice"]}])
    assert add_operator4.expression == {
        "$add": ["$price", {"$multiply": ["$quantity", "$unitPrice"]}]
    }


def test_add_factory_function():
    """Test that the add factory function works correctly."""
    # Test with two arguments
    add_op1 = add(5, 10)
    assert add_op1.expression == {"$add": [5, 10]}

    # Test with multiple arguments
    add_op2 = add("$price", "$tax", "$shipping")
    assert add_op2.expression == {"$add": ["$price", "$tax", "$shipping"]}

    # Verify it returns the correct type
    assert isinstance(add_op1, Add)
    assert isinstance(add_op2, Add)
