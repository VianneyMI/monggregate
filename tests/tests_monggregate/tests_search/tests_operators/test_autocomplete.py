def test_autocomplete_expression():
    # Setup
    from monggregate.search.operators.autocomplete import Autocomplete, TokenOrderEnum

    autocomplete = Autocomplete(
        query="hel",
        path="name"
    )

    # Act
    result = autocomplete.expression

    # Assert
    assert result == {
        "autocomplete": {
            "query": "hel",
            "path": "name",
            "tokenOrder": "any",
            "fuzzy": None,
            "score": None
        }
    }


# TODO
