from monggregate.search.operators.operator import SearchOperator

def test_search_operator_instantiation():
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
