"""Module to test compound examples.

As presented here : https://www.mongodb.com/docs/atlas/atlas-search/compound/
"""
from datetime import datetime
from monggregate.pipeline import Pipeline, Search, SearchMeta, Compound, Facet
from monggregate.search.collectors.facet import NumericFacet, StringFacet, DateFacet

def test_facet():
    """Test facet example."""

    expected_statement = {
    "$searchMeta": {
        "index": "movies", 
        "highlight": None, 
        "count": None, 
        "returnStoredSource": False, 
        "scoreDetails": False,
      "facet": {
        "operator": {
          "range": {
            "path": "released",
            "gte": datetime(year=2000, month=1, day=1),
            "lte": datetime(year=2015, month=1, day=31),
            "score":None
          }
        },
        "facets": {
          "directorsFacet": {
            "type": "string",
            "path": "directors",
            "numBuckets" : 7
          },
          "yearFacet" : {
            "type" : "number",
            "path" : "year",
            "boundaries" : [2000,2005,2010, 2015],
            "default":None
          }
        }
      }
    }
  }

    pipeline = Pipeline()

    pipeline.search_meta(
    index="movies",
    collector_name="facet", 
    operator=Search.Range(
        path="released", 
        gte=datetime(year=2000, month=1, day=1), 
        lte=datetime(year=2015, month=1, day=31)
        ),
    facets=[
        StringFacet(name="directorsFacet", path="directors", num_buckets=7),
        NumericFacet(name="yearFacet", path="year", boundaries=[2000, 2005, 2010, 2015]),
    ]

)
    assert pipeline.export()[0] == expected_statement, pipeline.export()[0]


if __name__ =="__main__":
    test_facet()