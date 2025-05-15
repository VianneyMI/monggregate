"""Tests for the Sort stage."""

import pytest
from monggregate.stages import Sort


class TestSort:
    """Tests for the Sort stage."""

    def test_instantiation(self) -> None:
        """Test that the Sort stage can be instantiated correctly."""

        sort = Sort(by="field1")
        assert isinstance(sort, Sort)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        sort = Sort(by="field1")
        assert sort.expression == {"$sort": {"field1": 1}}

    def test_expression_with_query(self) -> None:
        """Test that the expression method returns the correct expression with a query."""

        sort = Sort(query={"field1": 1})
        assert sort.expression == {"$sort": {"field1": 1}}

        sort = Sort(query={"field1": 1, "field2": -1})
        assert sort.expression == {"$sort": {"field1": 1, "field2": -1}}

    def test_expression_with_ascending_as_list_of_strings(self) -> None:
        """Test that the expression method returns the correct expression with ascending and descending."""

        sort = Sort(ascending=["field1"])
        assert sort.expression == {"$sort": {"field1": 1}}

    def test_expression_with_ascending_as_dict(self) -> None:
        """Test that the expression method returns the correct expression with ascending and descending."""

        sort = Sort(ascending={"field1": 1})
        assert sort.expression == {"$sort": {"field1": 1}}

    def test_expression_with_ascending_as_bool_only(self) -> None:
        """Test that the expression method returns the correct expression with ascending and descending."""

        with pytest.raises(ValueError):
            Sort(ascending=True)

    def test_expression_with_ascending_as_bool_with_query(self) -> None:
        """Test that the expression method returns the correct expression with ascending and descending."""

        sort = Sort(ascending=True, query={"field1": 1})
        assert sort.expression == {"$sort": {"field1": 1}}

    def test_expression_with_ascending_descending_as_list_of_strings(self) -> None:
        """Test that the expression method returns the correct expression with ascending and descending."""

        sort = Sort(ascending=["field1"], descending=["field2"])
        assert sort.expression == {"$sort": {"field1": 1, "field2": -1}}

    @pytest.mark.xfail(
        reason="Should raise a ValueError/ValidationError but raises a KeyError. "
    )
    def test_expression_with_ascending_descending_as_bool(self) -> None:
        """Test that the expression method returns the correct expression with ascending and descending."""

        # The error that prevents passing both ascending an descending as booleans
        # is caught by pydantic, that continues to the next validator.
        # Where ascending is received as None as it hasn't passed the validation.

        with pytest.raises(ValueError):
            Sort(ascending=True, descending=True, by=["field1"])
