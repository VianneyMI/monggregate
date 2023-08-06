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


if __name__ == "__main__":
    tests = TestSearchPipeline()
    tests.test_autocomplete()
    print("Everything passed")
