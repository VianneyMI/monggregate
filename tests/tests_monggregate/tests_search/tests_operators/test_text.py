from monggregate.search.operators.text import Text

def test_text_expression_with_fuzzy_and_synonyms():
    # Setup
    text_op = Text(
        query="mongodb atlas",
        path="description",
        score={"boost": 3},
        synonyms="mySynonyms"
    )
    expected = {
        "text": {
            "query": "mongodb atlas",
            "path": "description",
            "score": {"boost": 3},
            "synonyms": "mySynonyms"
        }
    }

    # Act
    expression = text_op.expression

    # Assert
    assert expression == expected