import pytest
from monggregate.search.operators.text import Text
from monggregate.search.commons.fuzzy import FuzzyOptions


def test_text_instantiation():
    """Test that Text search operator can be instantiated correctly."""
    # Test with basic configuration
    text_operator = Text(query="mongodb", path="description")

    expected_expression = {"text": {"query": "mongodb", "path": "description"}}

    assert text_operator.expression == expected_expression

    # Test with multiple paths
    text_operator2 = Text(query="database", path=["title", "description", "tags"])

    expected_expression2 = {
        "text": {"query": "database", "path": ["title", "description", "tags"]}
    }

    assert text_operator2.expression == expected_expression2

    # Test with fuzzy options
    text_operator3 = Text(
        query="aggregation",
        path="content",
        fuzzy=FuzzyOptions(maxEdits=2, prefixLength=0),
    )

    expected_expression3 = {
        "text": {
            "query": "aggregation",
            "path": "content",
            "fuzzy": {"maxEdits": 2, "prefixLength": 0},
        }
    }

    assert text_operator3.expression == expected_expression3

    # Test with synonyms
    text_operator4 = Text(
        query="document", path=["title", "abstract"], synonyms="database_terms"
    )

    expected_expression4 = {
        "text": {
            "query": "document",
            "path": ["title", "abstract"],
            "synonyms": "database_terms",
        }
    }

    assert text_operator4.expression == expected_expression4
