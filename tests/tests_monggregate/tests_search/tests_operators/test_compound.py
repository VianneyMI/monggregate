"""Tests for `monggregate.search.operators.compound` module."""

from monggregate.search.operators.compound import Compound


def test_compound_expression_with_must_equals() -> None:
    """Tests that the compound expression is correct when using the must equals operator."""

    # Setup
    compound = Compound()
    path = "field"
    value = "test"
    compound.equals("must", path=path, value=value)

    expected_expression = {
        "compound": {
            "must": [{"equals": {"path": path, "score": None, "value": value}}]
        }
    }

    # Act
    actual_expression = compound.expression

    # Assert
    assert actual_expression == expected_expression
