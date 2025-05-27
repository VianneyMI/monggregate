"""Module to test compound examples.

As presented here : https://www.mongodb.com/docs/atlas/atlas-search/compound/
"""

from monggregate.pipeline import Pipeline, Search, SearchMeta, Compound, Facet
from monggregate.search.collectors.facet import NumericFacet, StringFacet, DateFacet

def test_must_and_must_not()->None:
    """Tests the must and must_not example."""


    expected_statement = {
        "$search": {
        "index": "fruits", 
        "highlight": None, 
        "count": None, 
        "returnStoredSource": False, 
        "scoreDetails": False,
        "compound": {
            "must": [{
            "text": {
                "query": "varieties",
                "path": "description"
            }
            }],
            "mustNot": [{
            "text": {
                "query": "apples",
                "path": "description"
            }
            }]
        }
        }
    }


    pipeline = Pipeline()
    pipeline.search(
        index="fruits", 
        operator_name="compound"
    ).search( 
        clause_type="must", 
        query="varieties", 
        path="description"
    ).search(
        clause_type="mustNot",
        query="apples",
        path="description"
    )

    assert pipeline.export()[0] == expected_statement, pipeline.export()[0]

def test_must_and_should()->None:
    """Test must and should clauses."""


    expected_statement = {
        "$search": {
        "index": "fruits", 
        "highlight": None, 
        "count": None, 
        "returnStoredSource": False, 
        "scoreDetails": False,
        "compound": {
            "must": [{
            "text": {
                "query": "varieties",
                "path": "description"
            }
            }],
            "should": [{
            "text": {
                "query": "Fuji",
                "path": "description"
            }
            }],
            'minimumShouldMatch': 0
        }
        }
    }

    pipeline = Pipeline()

    pipeline.search(
    index="fruits",
    operator_name="compound"
    ).search(
        clause_type="must",
        query="varieties",
        path="description"
    ).search(
        clause_type="should",
        query="Fuji",
        path="description"
    )

    assert pipeline.export()[0] == expected_statement, pipeline.export()[0]

def test_minimum_should_match()->None:
    """Test minimum should match clause."""


    expected_statement = {
        "$search": {
        "index": "fruits", 
        "highlight": None, 
        "count": None, 
        "returnStoredSource": False, 
        "scoreDetails": False,
        "compound": {
        "must": [{
          "text": {
             "query": "varieties",
             "path": "description"
          }
        }],
        "should": [
          {
            "text": {
              "query": "Fuji",
              "path": "description"
            }
          },
          {
            "text": {
              "query": "Golden Delicious",
              "path": "description"
            }
          }],
          "minimumShouldMatch": 1
        }
      }
    }
    
    pipeline = Pipeline()

    pipeline.search(
            index="fruits",
            operator_name="compound",
            minimum_should_match=1
        ).search( 
            path="description",
            query="varieties",
            clause_type="must"
        ).search(
            path="description", 
            query="Fuji"
        ).search(
            path="description", 
            query="Golden Delicious",
        )

    assert pipeline.export()[0] == expected_statement, pipeline.export()[0]

def test_filter()->None:
    """Test filter examples."""

    expected_statement = {
        "$search": {
        "index": "fruits", 
        "highlight": None, 
        "count": None, 
        "returnStoredSource": False, 
        "scoreDetails": False,
        "compound": {
        "must": [{
          "text": {
            "query": "varieties",
            "path": "description"
          }
        }],
        "should": [{
          "text": {
            "query": "banana",
            "path": "description"
          }
        }],
        "filter": [{
          "text": {
            "query": "granny",
            "path": "description"
          },
          
        }],
        "minimumShouldMatch": 0
      }
    }
    }
    

    pipeline = Pipeline()

    pipeline.search(
        index="fruits",
        operator_name="compound"
    ).search(
        clause_type="must",
        path="description", 
        query="varieties"
    ).search(
        clause_type="should",
        path="description", 
        query="banana"
    ).search(
        clause_type="filter",
        path="description", 
        query="granny"
    )

    assert pipeline.export()[0] == expected_statement, pipeline.export()[0]


def test_nested()->None:
    """Test nested examples."""

    expected_statement = {
        "$search": {
        "index": "fruits", 
        "highlight": None, 
        "count": None, 
        "returnStoredSource": False, 
        "scoreDetails": False,
        "compound": {
        "should": [
          {
            "text": {
              "query": "apple",
              "path": "type"
            }
          },
          {
            "compound": {
              "must": [
                {
                  "text": {
                    "query": "organic",
                    "path": "category"
                  }
                },
                {
                  "equals": {
                    "value": True,
                    "path": "in_stock",
                    "score":None # TODO: Investigate this
                  }
                }
              ]
            }
          }
        ],
        "minimumShouldMatch": 1
      }
    }
    }
    
    

    pipeline = Pipeline()

    pipeline.search(
        index="fruits",
        operator_name="compound",
        minimum_should_match=1
    ).search(
        clause_type="should",
        path="type", 
        query="apple"
    ).search(
        clause_type="should",
        operator_name="compound",
        must=[
            Search.Text(query="organic", path="category"),
            Search.Equals(path="in_stock", value=True) 
        ]
    )

    assert pipeline.export()[0] == expected_statement, pipeline.export()[0]


if __name__ == "__main__":
    test_must_and_must_not()
    test_must_and_should()
    test_minimum_should_match()
    test_filter()
    test_nested()
