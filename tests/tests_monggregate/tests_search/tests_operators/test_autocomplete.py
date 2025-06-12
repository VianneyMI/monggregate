import pytest
from monggregate.search.operators.autocomplete import Autocomplete
from monggregate.search.commons import FuzzyOptions

def test_autocomplete_expression():
    # Setup
    query = "test"
    path = "field"
    fuzzy_options = FuzzyOptions(maxEdits=1, prefixLength=1, maxExpansions=10)

    autocomplete = Autocomplete(
        query=query,
        path=path,
        token_order="any",
        fuzzy=fuzzy_options,
        score={"boost": 2}
    )

    expected_expression = {
        "autocomplete": {
            "query": query,
            "path": path,
            "tokenOrder": "any",
            "fuzzy": {
                "maxEdits": 1,
                "prefixLength": 1,
                "maxExpansions": 10
            },
            "score": {"boost": 2}
        }
    }

    # Act
    actual_expression = autocomplete.expression

    # Assert
    assert actual_expression == expected_expression



# TODO
