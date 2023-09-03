"""Module gathering the tests of the array operators"""

# pylint: disable=redefined-builtin
 # pylint: disable=import-error
import pytest
from monggregate.operators.array import(
    ArrayToObject, array_to_object,
    Filter, filter,
    First, first,
    In, in_,
    IsArray, is_array,
    Last, last,
    MaxN, max_n,
    MinN, min_n,
    Size, size,
    SortArray, sort_array

)
# The below is imported to create a more complex test case
# but will not be tested in this module
from monggregate.operators.comparison import greather_than

@pytest.mark.operators
@pytest.mark.unit
@pytest.mark.functional
class TestArrayOperators:
    """This class only aims at reusing the markers"""

    def test_array_to_object(self)->None:
        """Tests the $arrayToObject operator class and mirror function"""

        array_to_object_op = ArrayToObject(expression="$dimensions")

        # Unit test
        # -----------------
        assert array_to_object_op

        # Functional test
        # -----------------
        assert array_to_object_op.statement == array_to_object("$dimensions").statement == {
            "$arrayToObject" :"$dimensions"
        }


    def test_filter(self)->None:
        """Tests $filter operator"""


        filter_op = Filter(
            expression = [1, 2, 3, 4],
            let = "num",
            query = greather_than("$$num", 2),
        )

        # Unit test
        # ---------------------
        assert filter_op

        # Functional test
        # ---------------------
        assert filter_op.statement  == filter(
            [1, 2, 3, 4],
            "num",
            greather_than("$$num", 2)
            ).statement == {
            "$filter" : {
                "input" : [1, 2, 3, 4],
                "as" : "num",
                "cond" : {
                    "$gt" : ["$$num", 2]
                },
                "limit":None
            }
        }

    def test_first(self)->None:
        """Tests $first operator class and mirror function"""


        first_op = First(
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert first_op

        # Functional test
        # ---------------------
        assert first_op.statement  == first([1, 2, 3, 4]).statement == {
            "$first" : [1, 2, 3, 4]
        }

    def test_in(self)->None:
        """Tests the $in operator class and mirror function"""

        in_op = In(
            left = 1,
            right = [1, 2, 3, 4]
        )

        # Unit test
        # -----------------------
        assert in_op

        # Functional test
        # -----------------------
        assert in_op.statement == in_(1, [1, 2, 3, 4]).statement == {
            "$in" : [1, [1, 2, 3, 4]]
        }

    def test_is_array(self)->None:
        """Tests the $isArray operator class and mirror function"""

        is_array_op = IsArray(expression=[1, 2, 3,4])

        # Unit test
        # --------------------
        assert is_array_op

        # Functional test
        # --------------------
        assert is_array_op.statement == is_array([1, 2, 3, 4]).statement == {
            "$isArray" : [1, 2, 3, 4]
        }

    def test_last(self)->None:
        """Tests $last operator class and mirror function"""


        last_op = Last(
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert last_op

        # Functional test
        # ---------------------
        assert last_op.statement  == last([1, 2, 3, 4]).statement == {
            "$last" : [1, 2, 3, 4]
        }


    def test_max_n(self)->None:
        """Tests the $maxN operator class and mirror function"""

        max_n_op = MaxN(
            limit = 1,
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # -------------------
        assert max_n_op

        # Functional test
        # --------------------
        assert max_n_op.statement == max_n([1, 2, 3, 4], 1).statement == {
            "$maxN" : {
                "n" : 1,
                "input" : [1, 2, 3, 4]
            }
        }

    def test_min_n(self)->None:
        """Tests the $minN operator class and mirror function"""

        min_n_op = MinN(
            limit = 1,
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # -------------------
        assert min_n_op

        # Functional test
        # --------------------
        assert min_n_op.statement == min_n([1, 2, 3, 4], 1).statement == {
            "$minN" : {
                "n" : 1,
                "input" : [1, 2, 3, 4]
            }
        }

    def test_size(self)->None:
        """Tests the $size operator class and mirror function"""

        size_op = Size(
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert size_op

        # Functional test
        # ---------------------
        assert size_op.statement == size([1, 2, 3, 4]).statement == {
            "$size" : [1, 2, 3, 4]
        }


    def test_sort_array(self)->None:
        """Tests the $sortArray operator class and mirror function"""

        sort_array_op = SortArray(
            expression ="$team",
            sort_by = {"name":1}
            )

        # Unit test
        # ---------------
        assert sort_array_op

        # Functional test
        # ----------------
        assert sort_array_op.statement == sort_array("$team", {"name":1}).statement == {
            "$sortArray" : {
                "input" : "$team",
                "sortBy" : {
                    "name" :1
                }
            }
        }
