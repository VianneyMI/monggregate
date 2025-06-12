from monggregate.search.operators.regex import Regex

def test_regex_expression_basic():
    # Setup (Arrange)
    regex_op = Regex(
        query="^Star.*",
        path="title",
        allow_analyzed_field=True,
        score={"constant": 1}
    )
    expected = {
        "regex": {
            "query": "^Star.*",
            "path": "title",
            "allowAnalyzedField": True,
            "score": {"constant": 1}
        }
    }

    # Act
    expression = regex_op.expression

    # Assert
    
    assert expression == expected