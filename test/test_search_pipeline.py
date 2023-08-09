"""Module to test search through pipeline"""

import pytest
from monggregate import Pipeline
from monggregate.search.commons.fuzzy import FuzzyOptions

@pytest.mark.search
@pytest.mark.unit
@pytest.mark.functional
@pytest.mark.pipeline
class TestSearchPipeline:
    """This class only aims at reusing the markers"""

    def test_autocomplete(self)->None:
        """Tests the autocomple operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="autocomplete",
            path="title",
            query="test",
            fuzzy=FuzzyOptions(),
            score={"boost": {"value": 1.0}},
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "autocomplete": {
                    "query": "test",
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
        }
        assert pipeline.export()[0] == expected_output


    def test_equals(self)->None:
        """Tests the equals operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="equals",
            path="title",
            value=10
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "equals": {
                    "path": "title",
                    "score": None,
                    "value": 10
                }
            }
        }
        assert pipeline.export()[0] == expected_output


    def test_exists(self)->None:
        """Tests the exists operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="exists",
            path="title"
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "exists": {
                    "path": "title",
                }
            }
        }
        assert pipeline.export()[0] == expected_output


    def test_more_like_this(self)->None:
        """Tests the moreLikeThis operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="more_like_this",
            like = {
                "_id": "5a934e000102030405000000",
            }
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "moreLikeThis": {
                    "like": {
                        "_id": "5a934e000102030405000000",
                    }
                }
            }
        }
        assert pipeline.export()[0] == expected_output


    def test_range(self)->None:
        """Tests the range operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="range",
            path="price",
            gte=10,
            lte=20
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "range": {
                    "path": "price",
                    "gte": 10,
                    "lte": 20,
                    "score": None
                }
            }
        }
        assert pipeline.export()[0] == expected_output  


    def test_regex(self)->None:
        """Tests the regex operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="regex",
            path="title",
            query="^test$",
            allow_analyzed_field=False,
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "regex": {
                    "path": "title",
                    "query": "^test$",
                    "allowAnalyzedField": False,
                    "score": None
                }
            }
        }
        assert pipeline.export()[0] == expected_output


    def test_text(self)->None:
        """Tests the text operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="text",
            query="test",
            path="description",
            fuzzy=FuzzyOptions(),
            score={"boost": {"value": 1.0}},
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "text": {
                    "query": "test",
                    "path": "description",
                    "fuzzy": {
                        "maxEdits": 2,
                        "maxExpansions": 50,
                        "prefixLength": 0
                    },
                    "score": {
                        "boost": {
                            "value": 1.0
                        }
                    }
                }
            }
        }
        assert pipeline.export()[0] == expected_output


    def test_wildcard(self)->None:
        """Tests the wildcard operator"""

        # generate test
        # --------------
        pipeline = Pipeline()
        pipeline.search(
            operator_name="wildcard",
            path="title",
            query="test*",
            allow_analyzed_field=False,
            fuzzy=FuzzyOptions(),
        )

        # Functional test
        # ---------------
        expected_output = {
            "$search": {
                "index":"default",
                "highlight":None,
                "count":None,
                "returnStoredSource":False,
                "scoreDetails":False,
                "wildcard": {
                    "query": "test*",
                    "path": "title",
                    "allowAnalyzedField": False
                }
            }
        }
        assert pipeline.export()[0] == expected_output

if __name__ == "__main__":
    tests = TestSearchPipeline()
    tests.test_autocomplete()
    tests.test_equals()
    tests.test_exists()
    tests.test_more_like_this()
    tests.test_range()
    tests.test_regex()
    tests.test_text()
    tests.test_wildcard()
    print("Everything passed")
