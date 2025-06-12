"""Tests for `monggregate.search.operators.operator` module."""

from monggregate.search.operators import OperatorMap
from monggregate.search.operators.operator import SearchOperator


def test_operator_map_operator_coverage() -> None:
    """Tests that all operators are present in the operator map."""

    # Setup
    operators_in_operator_map = set(OperatorMap.values())
    operators_in_search_operators = set(SearchOperator.__subclasses__())

    # Act
    missing_operators_in_operator_map = (
        operators_in_search_operators - operators_in_operator_map
    )

    # Assert
    assert not missing_operators_in_operator_map, (
        f"Operators in search operators but not in operator map: {missing_operators_in_operator_map}"
    )


def test_search_operator_instantiation() -> None:
    # Setup
    class ConcreteOperator(SearchOperator):
        field: str

        @property
        def expression(self) -> dict:
            """Concrete implementation of the expression property"""
            return {"field": self.field}

    operator = ConcreteOperator(field="value")

    # Act
    result = operator.expression

    # Assert
    assert result == {"field": "value"}
