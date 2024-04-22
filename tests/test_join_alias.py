"""
Temporary test module to test join aliases

It is temporary as it should come in a more general test_pipeline module or package.
"""

from monggregate import Pipeline
from monggregate.stages import Lookup, Match

def test_left_join()->None:
    """Tests left join in pipeline class"""

    pipeline = Pipeline(collection="left")
    pipeline.join(
        other = "right",
        how = "left",
        on = "zipcode"
    )

    assert len(pipeline.stages) == 4, pipeline
    assert isinstance(pipeline[0], Lookup)
    assert pipeline[0]() == {
        "$lookup":{
            "from" : "right", # from references the right collection
            "localField" : "zipcode",
            "foreignField" : "zipcode",
            "as" : "__right__"
    }}


def test_inner_join()->None:
    """Tests left join in pipeline class"""

    pipeline = Pipeline(collection="left")
    pipeline.join(
        other = "right",
        how = "inner",
        on = "zipcode"
    )

    assert len(pipeline.stages) == 5, pipeline
    assert isinstance(pipeline[0], Lookup)

    # The only difference with Left join is that there is an additional Match stage
    # in order to filter out documents from left, with no matches in right.

    assert isinstance(pipeline[1], Match)
    assert pipeline[0]() == {
        "$lookup":{
            "from" : "right", # from references the right collection
            "localField" : "zipcode",
            "foreignField" : "zipcode",
            "as" : "__right__"
    }}

if __name__ == "__main__":
    test_left_join()
    test_inner_join()
