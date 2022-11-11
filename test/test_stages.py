"""
Module unit testing the stages.

Checks that at least each stage can be instantiated properly.

"""

import pytest
from pydantic import ValidationError

from monggregate import Pipeline
from monggregate import( # pylint: disable=import-error
    Stage,
    BucketAuto,
    Bucket,
    Count,
    Group,
    Limit,
    Lookup,
    Match,
    Out,
    Project,
    ReplaceRoot,
    Sample,
    Set,
    Skip,
    SortByCount,
    Sort,
    Unwind
)

State = dict[str, Stage]

@pytest.mark.stages
@pytest.mark.unit
@pytest.mark.functional
class TestStages:
    """This class only aims at reusing the markers"""

    @pytest.fixture(autouse=True, scope="class")
    def state(self)->State:
        """
        Creates a memory for the tests.

        DISCLAIMER : This is considered bad practice.
                     However, the unit tests are still independent from one another.
                     Using the state to avoid code repetition in the functional tests
                     Besides, the functional tests are still independent from one another.
                     Each functional test will depend on its equivalent unit test.
                     Downside is that if the all the tests are launched, the unit tests will be run
                     several times.
                     Thus the test suite should either be run using at least one of the markers (unit, functional)
        """
        return {}

    def test_stage(self)->None:
        """Testes the stage parent class"""

        with pytest.raises(TypeError):
            # Checking that Stage cannot be instantiated
            stage = Stage(statement={})  # pylint: disable=abstract-class-instantiated


    def test_bucket_auto(self, state:State)->None:
        """Testes $bucketAuto stage class and mirror function"""

        bucket_auto = BucketAuto(
            group_by="test",
            buckets=10
        )
        assert bucket_auto
        state["bucket_auto"] = bucket_auto

        assert BucketAuto(
            group_by="test",
            buckets = 4,
            output = {"new_var":{"$sum":"my_expression"}},
            granularity="E12"
        )


    def test_bucket(self, state:State)->None:
        """Testes the $bucket stage class and mirror function"""

        bucket = Bucket(
            group_by="income",
            boundaries=[25000, 40000, 60000, 100000],
        )
        assert bucket
        state["bucket"] = bucket

        assert Bucket(
            group_by="income",
            boundaries=[25000, 40000, 60000, 100000],
            default="other"
        )


        assert Bucket(
            group_by="income",
            boundaries=[25000, 40000, 60000, 100000],
            default="other",
            output={"output":"expression"}
        )



    def test_count(self, state:State)->None:
        """Testes the count stage"""

        count = Count(name="count")
        assert count
        state["count"] = count

    def test_group(self, state:State)->None:
        """Testes the group stage"""

        # Testing mandatory fields
        # ------------------------
        group = Group(
            query = {"_id":"count"}
        )
        assert group
        state["group"] = group

        # Tests aliases
        # -----------------------
        assert Group(
            _id="count"
        )

        # Test optional arguments
        # ------------------------
        assert Group(
            by="count",
            query = {
                "output":{"$sum":"income"}
            }
        )


    def test_limit(self, state:State)->None:
        """Testes the limit stage"""

        limit = Limit(value=10)
        assert limit
        state["limit"] = limit


    def test_lookup(self, state:State)->None:
        """Testes the lookup stage"""

        # Testing mandatory attributes
        # -----------------------------
        lookup = Lookup(
            right = "other_collection",
            left_on = "_id",
            right_on = "foreign_key",
            name = "matches"
        )
        assert lookup
        state["lookup"] = lookup

        assert  Lookup(
            right = "restaurants",
            left_on = "restaurant_name",
            right_on = "name",
            let = {"orders_drink":"$drink"},
            pipeline = [
                {
                    "$match" : {
                        "$expr" : {
                            "$in" : ["$$orders_drink", "$beverages"]
                        }
                    }
                }
            ],
            name = "matches"
        )


        # Testing aliases
        # -----------------------------
        params = {
            "from" : "other_collection",
            "local_field" : "_id",
            "foreign_field" : "foreign_key",
            "as" :"matches"
        }
        simple = Lookup(**params)
        assert simple

        # Testing optional attributes
        # -----------------------------
        uncorrelated = Lookup(
            right = "other_collection",
            pipeline = [],
            name = "new_fields"
        )
        assert uncorrelated


    def test_match(self, state:State)->None:
        """Testes the match stage"""

        match = Match(query={"_id":"123455"})
        assert match
        state["match"] = match

    def test_out(self, state:State)->None:
        """Testes the out stage"""

        out = Out(coll="my_collection")
        assert out
        state["out"] = out

        # Test aliases
        # ---------------
        assert Out(collection="my_collection")

        # Test optional attributes
        # ----------------
        assert Out(db="other_db", coll="new_collection")



    def test_project(self, state:State)->None:
        """Testes the project stage"""

        # Testing mandatory attributes
        # -----------------------------
        project = Project(projection={"_id":0}) #projection is not really mandatory
        assert project
        state["proejct"] = project

        with pytest.raises(ValidationError):
            Project()

        with pytest.raises(ValidationError):
            Project(projection={})

        # Testing aliases
        # -----------------------------
        assert Project(
            fields = "email",
            include = True
        )


        # Testing optional attributes
        # -----------------------------
            # Include/Exclude as set
        assert Project(
            include=set(["name"])
        )

        assert Project(
            exclude=set(["password"])
        )
            # Include/Exclude as str or list of strings
        assert Project(
            include=set(["name"])
        )

        assert Project(
            exclude=["name", "_id"]
        )

        #TODO: test with string parameters and list


    def test_replace_root(self, state:State)->None:
        """Testes the replace_root stage"""

        # Testing mandatory attributes
        # -----------------------------
        replace_root = ReplaceRoot(path_to_new_root="myarray.mydocument")
        assert replace_root
        state["replace_root"] = replace_root

        # Testing aliases
        # -----------------------------
        replace_root = ReplaceRoot(path="myarray.mydocument")
        assert replace_root

        # Testing optional attributes
        # -----------------------------
        # N/A

    def test_sample(self, state:State)->None:
        """Testes the sample stage"""

        # Testing mandatory attributes
        # -----------------------------
        sample = Sample(value=3) # value is not really mandatory
        assert sample
        state["sample"] = sample

        # Testing aliases
        # -----------------------------
        # N/A

        # Testing optional attributes
        # -----------------------------
        sample = Sample() # sample has no mandatory field
                        # however it has a default

        assert sample
        assert sample.value == 10



    def test_set(self, state:State)->None:
        """Testes the xxx stage"""

        # Testing mandatory attributes
        # -----------------------------
        set = Set(document={
            "field1":"value1",
            "fieldN":"valueN"
        })
        assert set
        state["set"] = set

        # Testing aliases
        # -----------------------------
        # N/A

        # Testing optional attributes
        # -----------------------------
        # N/A


    def test_skip(self, state:State)->None:
        """Testes the skip stage"""

        # Testing mandatory attributes
        # -----------------------------
        skip = Skip(value=10)
        assert skip
        state["skip"] = skip

        # Testing aliases
        # -----------------------------
        # N/A

        # Testing optional attributes
        # -----------------------------
        # N/A


    def test_sort_by_count(self, state:State)->None:
        """Testes the sort_by_count stage"""

        # Testing mandatory attributes
        # -----------------------------
        sort_by_count = SortByCount(
            by = "name"
        )
        assert sort_by_count
        state["sort_by_count"] = sort_by_count

        # Testing aliases
        # -----------------------------
        # N/A

        # Testing optional attributes
        # -----------------------------
        # N/A


    def test_sort(self, state:State)->None:
        """Testes the sort stage"""

        # Testing mandatory attributes
        # -----------------------------
        with pytest.raises(ValidationError):
            sort = Sort(query={"field1":1, "fieldN":0})

        with pytest.raises(ValidationError):
            sort = Sort(query={})

        sort = Sort(query={"field1":1, "fieldN":-1})
        assert sort
        state["sort"] = sort

        # Testing aliases
        # -----------------------------
        assert Sort(
            by = "count"
        )

        # Testing optional attributes
        # -----------------------------
        assert Sort(ascending=set(["field1", "field2"]))
        assert Sort(descending=set(["field1"]))
        assert Sort(
            ascending=set(["field1", "field2"]),
            descending=set(["field3", "fieldN"])
            )


    def test_unwind(self, state:State)->None:
        """Testes the $unwind stage"""

        # Testing mandatory attributes
        # -----------------------------
        unwind = Unwind(
            path_to_array = "xyz",
        )
        assert unwind
        state["unwind"] = unwind

        # Testing aliases
        # -----------------------------
        assert Unwind(
            path = "xyz"
        )

        # Testing optional attributes
        # -----------------------------
        assert Unwind(
            path = "xyz",
            include_array_index = "index",
            always = True
        )


@pytest.mark.latest
class TestStagesFunctional(TestStages):
    """This class gather the functional tests of the stages"""


    def test_bucket_auto_statement(self, state:State)->None:
        """Testes the BucketAuto class statement and its mirror function"""

        assert state["bucket_auto"].statement == Pipeline().bucket_auto(
            by = "test",
            buckets = 10
        )[-1].statement == {
            "$bucketAuto" : {
                "groupBy" : "$test",
                "buckets" : 10,
                "output" : None,
                "granularity" : None
                }
            }

    def test_bucket_statement(self, state:State)->None:
        """
        Testes the Bucket class statement and its mirror function
        """

        bucket = state["bucket"]
        assert bucket.statement == Pipeline().bucket(
            by = "income",
            boundaries = [25000, 40000, 60000, 100000])[-1].statement == {
            "$bucket" : {
                "groupBy" : "$income",
                "boundaries" : [25000, 40000, 60000, 100000],
                "default" : None,
                "output" : None
            }
        }

# ------------------------
# Debugging:
#-------------------------
if __name__ == "__main__":
    TestStages().test_stage()
    TestStages().test_bucket_auto({})
    TestStages().test_bucket({})
    TestStages().test_count({})
    TestStages().test_group({})
    TestStages().test_limit({})
    TestStages().test_match({})
    TestStages().test_out({})
    TestStages().test_project({})
    TestStages().test_replace_root({})
    TestStages().test_sample({})
    TestStages().test_set({})
    TestStages().test_skip({})
    TestStages().test_sort_by_count({})
    TestStages().test_sort({})
