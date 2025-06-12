"""Tests for `monggregate.search.operators.clause` module."""

from monggregate.search.operators.clause import Clause
from monggregate.search.operators.compound import Compound
from monggregate.search.operators import OperatorMap


def test_consistency_with_operator_map() -> None:
    """Tests that all operators are present in the clause type."""

    # Setup
    operators_in_clause = set(Clause.__args__) | {Compound}
    # Compoound should be in Clause but it seems complex to implement right now
    # TODO : Fix this when fully migrating to pydantic v2.
    operators_in_operator_map = set(OperatorMap.values())

    # Act
    missing_operators_in_clause = operators_in_operator_map - operators_in_clause
    missing_operators_in_operator_map = operators_in_clause - operators_in_operator_map

    # Assert
    assert not missing_operators_in_clause, (
        f"Operators in operator map but not in clause: {missing_operators_in_clause}"
    )
    assert not missing_operators_in_operator_map, (
        f"Operators in clause but not in operator map: {missing_operators_in_operator_map}"
    )
