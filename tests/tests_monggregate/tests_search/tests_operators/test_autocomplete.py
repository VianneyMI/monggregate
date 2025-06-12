from monggregate.search.operators.autocomplete import Autocomplete, TokenOrderEnum

def test_autocomplete_expression():
    # Setup
    query = "some_query"
    path = "some_field"
    expected_expression = {
        "autocomplete": {
            "query": query,
            "path": path,
            "tokenOrder": "any",
            "fuzzy": None,
            "score": None
        }
    }

    # Act
    autocomplete_op = Autocomplete(query=query, path=path)
    result_expression = autocomplete_op.expression


    # Assert
    assert result_expression == expected_expression


class TestAutocomplete:
    """Tests for `Autocomplete` class."""

    def test_instantiation(self) -> None:
        """Test that `Autocomplete` class can be instantiated."""
        query = "some_query"
        path = "some_field"
        auto = Autocomplete(query=query, path=path)
        assert isinstance(auto, Autocomplete)

    def test_expression_basic(self) -> None:
        """Test basic expression output of `Autocomplete` class."""
        query = "some_query"
        path = "some_field"
        auto = Autocomplete(query=query, path=path)
        assert auto.expression == {
            "autocomplete": {
                "query": query,
                "path": path,
                "tokenOrder": "any",
                "fuzzy": None,
                "score": None
            }
        }




# TODO
