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
