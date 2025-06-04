"""Test the base classes for search stages."""

import pytest

from monggregate.stages.search.base import BaseModel, SearchBase, SearchConfig
from monggregate.search.operators.operator import OperatorLiteral
from monggregate.search.operators import OperatorMap
from monggregate.search.collectors import Facet


class TestSearchConfig:
    """Tests for the `SearchConfig` class."""

    def test_instantiation(self) -> None:
        """Tests instantiation of the SearchConfig class."""

        config = SearchConfig()
        assert isinstance(config, SearchConfig)
        assert isinstance(config, BaseModel)

    def test_expression(self) -> None:
        """Tests the expression property of the SearchConfig class.

        Currently the expression property is not implemented because it does not make sens.
        The question is then should SearchConfig really inherit from BaseModel?
        or should it inherit from pydantic.BaseModel?
        or should it be an abstract class?
        """

        config = SearchConfig()
        with pytest.raises(NotImplementedError):
            config.expression


class TestSearchBase:
    """Tests for the `SearchBase` class."""

    default_args = {
        "path": "field",
        "query": "query",
        "value": "value",
        "gte": 1,
        "lte": 2,
    }

    def test_instantiation(self) -> None:
        """Tests instantiation of the SearchBase class."""

        base = SearchBase()
        assert isinstance(base, SearchBase)
        assert isinstance(base, BaseModel)

    @pytest.mark.xfail(
        reason="""Broken because operator is not correctly set.
                Uncomment lines in init to fix."""
    )
    @pytest.mark.parametrize("operator_name", OperatorLiteral.__args__)
    def test_init_with_operator_name(self, operator_name: OperatorLiteral) -> None:
        """Tests the init method of the SearchBase class."""

        search_base = SearchBase(operator_name=operator_name, **self.default_args)
        assert isinstance(search_base.operator, OperatorMap[operator_name])

    @pytest.mark.xfail(
        reason="""Broken because collector is not correctly set.
                Uncomment lines in init to fix."""
    )
    def test_init_with_collector_name(self, collector_name: str = "facet") -> None:
        """Tests the init method of the SearchBase class."""

        search_base = SearchBase(collector_name=collector_name)
        assert isinstance(search_base.collector, Facet)

    def test_validate_operator(self) -> None:
        """Tests the validate_operator method of the SearchBase class."""

        assert False

    def test_expression(self) -> None:
        """Tests the expression method of the SearchBase class."""

        assert False

    def test_from_operator(self) -> None:
        """Tests the from_operator method of the SearchBase class."""

        assert False

    def test_init_autocomplete(self) -> None:
        """Tests the init_autocomplete method of the SearchBase class."""

        assert False

    def test_init_compound(self) -> None:
        """Tests the init_compound method of the SearchBase class."""

        assert False

    def test_init_equals(self) -> None:
        """Tests the init_equals method of the SearchBase class."""

        assert False

    def test_init_exists(self) -> None:
        """Tests the init_exists method of the SearchBase class."""

        assert False

    def test_init_facet(self) -> None:
        """Tests the init_facet method of the SearchBase class."""

        assert False

    def test_init_more_like_this(self) -> None:
        """Tests the init_more_like_this method of the SearchBase class."""

        assert False

    def test_init_range(self) -> None:
        """Tests the init_range method of the SearchBase class."""

        assert False

    def test_init_regex(self) -> None:
        """Tests the init_regex method of the SearchBase class."""

        assert False

    def test_init_string(self) -> None:
        """Tests the init_string method of the SearchBase class."""

        assert False

    def test_init_text(self) -> None:
        """Tests the init_text method of the SearchBase class."""

        assert False

    def test_init_wildcard(self) -> None:
        """Tests the init_wildcard method of the SearchBase class."""

        assert False

    def test_Autocomplete(self) -> None:
        """Tests the Autocomplete method of the SearchBase class."""

        assert False

    def test_Compound(self) -> None:
        """Tests the Compound method of the SearchBase class."""

        assert False

    def test_Equals(self) -> None:
        """Tests the Equals method of the SearchBase class."""

        assert False

    def test_Exists(self) -> None:
        """Tests the Exists method of the SearchBase class."""

        assert False

    def test_Facet(self) -> None:
        """Tests the Facet method of the SearchBase class."""

        assert False

    def test_MoreLikeThis(self) -> None:
        """Tests the MoreLikeThis method of the SearchBase class."""

        assert False

    def test_Range(self) -> None:
        """Tests the Range method of the SearchBase class."""

        assert False

    def test_Regex(self) -> None:
        """Tests the Regex method of the SearchBase class."""

        assert False

    def test_Text(self) -> None:
        """Tests the Text method of the SearchBase class."""

        assert False

    def test_Wildcard(self) -> None:
        """Tests the Wildcard method of the SearchBase class."""

        assert False

    def test_autocomplete(self) -> None:
        """Tests the autocomplete method of the SearchBase class."""

        assert False

    def test_equals(self) -> None:
        """Tests the equals method of the SearchBase class."""

        assert False

    def test_exists(self) -> None:
        """Tests the exists method of the SearchBase class."""

        assert False

    def test_more_like_this(self) -> None:
        """Tests the more_like_this method of the SearchBase class."""

        assert False

    def test_range(self) -> None:
        """Tests the range method of the SearchBase class."""

        assert False

    def test_regex(self) -> None:
        """Tests the regex method of the SearchBase class."""

        assert False

    def test_text(self) -> None:
        """Tests the text method of the SearchBase class."""

        assert False

    def test_wildcard(self) -> None:
        """Tests the wildcard method of the SearchBase class."""

        assert False

    def test_set_minimum_should_match(self) -> None:
        """Tests the set_minimum_should_match method of the SearchBase class."""

        assert False

    def test_compound(self) -> None:
        """Tests the compound method of the SearchBase class."""

        assert False

    def test_must(self) -> None:
        """Tests the must method of the SearchBase class."""

        assert False

    def test_should(self) -> None:
        """Tests the should method of the SearchBase class."""

        assert False

    def test_must_not(self) -> None:
        """Tests the must_not method of the SearchBase class."""

        assert False

    def test_filter(self) -> None:
        """Tests the filter method of the SearchBase class."""

        assert False

    def test_facet(self) -> None:
        """Tests the facet method of the SearchBase class."""

        assert False

    def test_numeric(self) -> None:
        """Tests the numeric method of the SearchBase class."""

    def test_date(self) -> None:
        """Tests the date method of the SearchBase class."""

        assert False

    def test_string(self) -> None:
        """Tests the string method of the SearchBase class."""

        assert False
