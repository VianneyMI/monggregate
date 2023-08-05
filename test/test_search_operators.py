"""Module gathering the tests of the search operators"""

import pytest
from monggregate.base import pyd
from monggregate.search.operators import(
    Autocomplete,
    Compound,
    Equals,
    Exists,
    MoreLikeThis,
    Range,
    Regex,
    Text,
    Wilcard
)
from monggregate.search.commons.fuzzy import FuzzyOptions
from monggregate.search.commons.highlight import HighlightOptions

@pytest.mark.operators
@pytest.mark.unit
@pytest.mark.functional
class TestSearchOperators:
    """This class only aims at reusing the markers"""

    def test_autocomplete(self)->None:
        """Tests the autocomplete operator"""

        # generate test
        # --------------
        autocomplete_op = Autocomplete(
            query = "m",
            path = "title",
            fuzzy=FuzzyOptions(),
            score={"boost": {"value": 1.0}},
        )

        # Unit test
        # --------------
        assert autocomplete_op

        # Functional test
        # ---------------
        assert autocomplete_op.statement == {
            "autocomplete": {
                "query": "m",
                "path": "title",
                "fuzzy": {
                    "maxEdits": 2,
                    "maxExpansions": 50,
                    "prefixLength": 0
                },
                "score": {
                    "boost": {
                        "value": 1.0
                    }
                },
                "tokenOrder": "any"
            }
        }

    # def test_compound(self)->None:
    #     """Tests the compound operator"""
        
    #     autocomplete = Autocomplete()

    def test_equals(self)->None:
        """Tests the equals operator"""

        # generate test
        # --------------
        equals_op = Equals(
            path = "title",
            value = 10
        )

        # Unit test
        # --------------
        assert equals_op

        # Functional test
        # ---------------
        assert equals_op.statement == {
            "equals": {
                "path": "title",
                "score": None,
                "value": 10
            }
        }

        with pytest.raises(pyd.ValidationError):
            Equals(
                path = "test",
                value = {}
            )

    def test_exists(self)->None:
        """Tests the exists operator"""

        exists_op = Exists(
            path = "title"
        )

        # Unit test
        # --------------
        assert exists_op

        # Functional test
        # ---------------
        assert exists_op.statement == {
            "exists": {
                "path": "title",
            }
        }
    
    def test_more_like_this(self)->None:
        """Tests the moreLikeThis operator"""

        more_like_this_op = MoreLikeThis(
            like = {
                "_id": "5a934e000102030405000000",
            }
        )

        # Unit test
        # --------------
        assert more_like_this_op

        # Functional test
        # ---------------
        assert more_like_this_op.statement == {
            "moreLikeThis": {
                "like": {
                    "_id": "5a934e000102030405000000",
                }
            }
        }

        with pytest.raises(pyd.ValidationError):
            MoreLikeThis(
                like = None
            )

        with pytest.raises(pyd.ValidationError):
            MoreLikeThis(
                like = []
            )

    def test_range(self)->None:
        """Tests the range operator"""

        range_op = Range(
            path = "price",
            gte = 10,
            lte = 20
        )

        # Unit test
        # --------------
        assert range_op

        # Functional test
        # ---------------
        assert range_op.statement == {
            "range": {
                "path": "price",
                "gte": 10,
                "lte": 20,
                "score": None
            }
        }

        with pytest.raises(pyd.ValidationError):
            Range(
                path = "price",
                gte = 10,
                score = {}
            )

    def test_regex(self)->None:
        """Tests the regex operator"""

        regex_op = Regex(
            path = "title",
            query= "^test$",
        )

        # Unit test
        # --------------
        assert regex_op

        # Functional test
        # ---------------
        assert regex_op.statement == {
            "regex": {
                "path": "title",
                "query": "^test$",
                "allowAnalyzedField": False,
                "score": None
            }
        }

    def test_text(self)->None:
        """Tests the text operator"""

        text_op = Text(
            path = "description",
            query = "test"
        )

        # Unit test
        # --------------
        assert text_op

        # Functional test
        # ---------------
        assert text_op.statement == {
            "text": {
                "query": "test",
                "path": "description"
            }
        }

    def test_wilcard(self)->None:
        """Tests the wilcard operator"""

        wilcard_op = Wilcard(
            path = "title",
            query = "test"
        )

        # Unit test
        # --------------
        assert wilcard_op

        # Functional test
        # ---------------
        assert wilcard_op.statement == {
            "wildcard": {
                "allowAnalyzedField": False,
                "path": "title",
                "query": "test",
            }
        }
      