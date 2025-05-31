"""Tests for the `search_meta` module."""

from monggregate.search.commons.fuzzy import FuzzyOptions
from monggregate.stages.search.search_meta import SearchMeta


class TestSearchMeta:
    """Tests for the `SearchMeta` class."""

    def test_expression(self) -> None:
        """Tests the `__init__` method of the `SearchMeta` class."""

        search_meta = SearchMeta.from_operator(
            operator_name="text",
            path="title",
            query="test",
            fuzzy=FuzzyOptions(
                enabled=True,
                max_edits=2,
            ),
        )

        expected_expression = {
            "$searchMeta": {
                "index": "default",
                "highlight": None,
                "count": None,
                "returnStoredSource": False,
                "scoreDetails": False,
                "text": {
                    "path": "title",
                    "query": "test",
                    "fuzzy": {
                        "maxExpansions": 50,
                        "prefixLength": 0,
                        "maxEdits": 2,
                    },
                },
            }
        }

        assert search_meta.expression == expected_expression
