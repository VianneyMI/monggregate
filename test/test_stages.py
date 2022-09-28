"""
Module unit testing the stages.

Checks that at least each stage can be instantiated properly.

"""

import pytest
from pydantic import ValidationError

from monggregate import( # pylint: disable=import-error
    Stage,
    BucketAuto,
    Bucket,
    Count,
    Group,
    Limit,
    Match,
    Out,
    Project,
    ReplaceRoot,
    Sample,
    Set,
    Skip,
    SortByCount,
    Sort
)

# ----------------------
# Units Tests
# ----------------------
@pytest.mark.unit
def test_()->None:
    """Testes the xxx stage"""

    # Testing mandatory attributes
    # -----------------------------


    # Testing aliases
    # -----------------------------


    # Testing optional attributes
    # -----------------------------
@pytest.mark.unit
def test_stage()->None:
    """Testes stage parent class"""

    with pytest.raises(TypeError):
        stage = Stage(statement={}) # checks that Stage cannot be instantiated

@pytest.mark.unit
def test_bucket_auto()->None:
    """Testes bucket_auto stage"""

    bucket_auto = BucketAuto(
        group_by="test",
        buckets=10
    )
    assert bucket_auto
    del bucket_auto # to ensure it does not interfer on 2nd test

    bucket_auto = BucketAuto(
        group_by="test",
        buckets = 4,
        output = {"new_var":{"$sum":"my_expression"}},
        granularity="E12"
    )

    assert bucket_auto

@pytest.mark.unit
def test_bucket()->None:
    """Testes the bucket stage"""

    bucket = Bucket(
        group_by="income",
        boundaries=[25000, 40000, 60000, 10000],
    )
    assert bucket
    del bucket

    bucket = Bucket(
        group_by="income",
        boundaries=[25000, 40000, 60000, 10000],
        default="other"
    )

    assert bucket
    del bucket

    bucket = Bucket(
        group_by="income",
        boundaries=[25000, 40000, 60000, 10000],
        default="other",
        output={"output":"expression"}
    )

    assert bucket

@pytest.mark.unit
def test_count()->None:
    """Testes the count stage"""

    count = Count(name="count")
    assert count

@pytest.mark.unit
def test_group()->None:
    """Testes the group stage"""

    group = Group(
        by="count"
    )
    assert group
    del group

    # Tests aliases
    # -----------------------
    group = Group(
        _id="count"
    )
    assert group
    del group

    # Test optional arguments
    # ------------------------
    group = Group(
        by="count",
        query = {
            "output":{"$sum":"income"}
        }
    )
    assert group

@pytest.mark.unit
def test_limit()->None:
    """Testes the limit stage"""

    limit = Limit(value=10)
    assert limit

@pytest.mark.unit
def test_match()->None:
    """Testes the match stage"""

    match = Match(query={"_id":"123455"})
    assert match

@pytest.mark.unit
def test_out()->None:
    """Testes the out stage"""

    out = Out(coll="my_collection")
    assert out
    del out

    # Test alias
    out = Out(collection="my_collection")
    assert out
    del out

    out = Out(db="other_db", coll="new_collection")
    assert out

@pytest.mark.unit
def test_project()->None:
    """Testes the project stage"""

    # Testing mandatory attributes
    # -----------------------------
    project = Project(projection={"_id":0}) #projection is not really mandatory
    assert project
    del project

    with pytest.raises(ValidationError):
        Project()

    # Testing aliases
    # -----------------------------
    # N/A

    # Testing optional attributes
    # -----------------------------
    project = Project(
        include=set(["name"])
    )
    assert project
    del project

    project = Project(
        exclude=set(["password"])
    )
    assert project

    # test with string parameters and list

@pytest.mark.unit
def test_replace_root()->None:
    """Testes the replace_root stage"""

    # Testing mandatory attributes
    # -----------------------------
    replace_root = ReplaceRoot(path_to_new_root="myarray.mydocument")
    assert replace_root
    del replace_root

    # Testing aliases
    # -----------------------------
    replace_root = ReplaceRoot(path="myarray.mydocument")
    assert replace_root

    # Testing optional attributes
    # -----------------------------
    # N/A

@pytest.mark.unit
def test_sample()->None:
    """Testes the sample stage"""

    # Testing mandatory attributes
    # -----------------------------
    sample = Sample(value=3) # value is not really mandatory
    assert sample
    del sample

    # Testing aliases
    # -----------------------------
    # N/A

    # Testing optional attributes
    # -----------------------------
    sample = Sample() # sample has no mandatory field
                      # however it has a default

    assert sample
    assert sample.value == 10
    del sample

@pytest.mark.unit
def test_set()->None:
    """Testes the xxx stage"""

    # Testing mandatory attributes
    # -----------------------------
    set = Set(document={
        "field1":"value1",
        "fieldN":"valueN"
    })
    assert set
    del set

    # Testing aliases
    # -----------------------------
    # N/A

    # Testing optional attributes
    # -----------------------------
    # N/A

@pytest.mark.unit
def test_skip()->None:
    """Testes the skip stage"""

    # Testing mandatory attributes
    # -----------------------------
    skip = Skip(value=10)
    assert skip
    del skip

    # Testing aliases
    # -----------------------------
    # N/A

    # Testing optional attributes
    # -----------------------------
    # N/A

@pytest.mark.unit
def test_sort_by_count()->None:
    """Testes the sort_by_count stage"""

    # Testing mandatory attributes
    # -----------------------------
    sort_by_count = SortByCount(
        by = "name"
    )
    assert sort_by_count
    del sort_by_count

    # Testing aliases
    # -----------------------------
    # N/A

    # Testing optional attributes
    # -----------------------------
    # N/A

@pytest.mark.unit
def test_sort()->None:
    """Testes the sort stage"""

    # Testing mandatory attributes
    # -----------------------------
    sort = Sort(query={"field1":1, "fieldN":0})
    assert sort
    del sort

    # Testing aliases
    # -----------------------------
    # N/A

    # Testing optional attributes
    # -----------------------------
    sort = Sort(ascending=set(["field1", "field2"]))
    assert sort
    del sort

    sort = Sort(descending=set(["field1"]))
    assert sort
    del sort

    sort = Sort(
        ascending=set(["field1", "field2"]),
        descending=set(["field3", "fieldN"])
        )
    assert sort

#-------------------------
# Functional Tests
#-------------------------


# ------------------------
# Debugging:
#-------------------------
if __name__ == "__main__":
    test_stage()
    test_bucket_auto()
    test_bucket()
    test_count()
    test_group()
    test_limit()
    test_match()
    test_out()
    test_project()
    test_replace_root()
    test_sample()
    test_set()
    test_skip()
    test_sort_by_count()
    test_sort()
