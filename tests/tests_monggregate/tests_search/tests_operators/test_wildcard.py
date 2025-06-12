from monggregate.search.operators.wildcard import Wildcard

def test_wildcard_expression_basic():
    # Setup
    wildcard_op = Wildcard(
        query="foo*bar?",
        path="content",
        allow_analyzed_field=True,
        score={"boost": 5}
    )

    expected = {
        "wildcard": {
            "query": "foo*bar?",
            "path": "content",
            "allowAnalyzedField": True,
            "score": {"boost": 5}
        }
    }

    # Act
    expression = wildcard_op.expression

    # Assert
    assert expression == expected