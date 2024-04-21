"""Module gathering the tests of the accumulators operators"""

# pylint: disable=redefined-builtin
import pytest
from monggregate.operators.accumulators import( # pylint: disable=import-error
    Average, average,
    Count, count,
    First, first,
    Last, last,
    Max, max,
    Min, min,
    Push, push,
    Sum, sum
)

@pytest.mark.operators
@pytest.mark.unit
@pytest.mark.functional
class TestAccumulatorOperators:
    """This class only aims at reusing the markers"""

    def test_average(self)->None:
        """Tests the $avg operator class and mirror function"""

        average_op = Average(
            operand = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert average_op

        # Functional test
        # ---------------------
        assert average_op.expression  == average([1, 2, 3, 4]).expression == {
            "$avg" : [1, 2, 3, 4]
        }

    def test_count(self)->None:
        """Tests the $count operator class and mirror function"""

        count_op = Count()

        # Unit test
        # ---------------------
        assert count_op

        # Functional test
        # ---------------------
        assert count_op.expression  == count().expression == {
            "$count" : {}
        }



    def test_first(self)->None:
        """Tests $first operator class and mirror function"""


        first_op = First(
            operand = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert first_op

        # Functional test
        # ---------------------
        assert first_op.expression  == first([1, 2, 3, 4]).expression == {
            "$first" : [1, 2, 3, 4]
        }


    def test_last(self)->None:
        """Tests $last operator class and mirror function"""


        last_op = Last(
            operand = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert last_op

        # Functional test
        # ---------------------
        assert last_op.expression  == last([1, 2, 3, 4]).expression == {
            "$last" : [1, 2, 3, 4]
        }

    def test_max(self)->None:
        """Tests $max operator class and mirror function"""


        max_op = Max(
            operand = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert max_op

        # Functional test
        # ---------------------
        assert max_op.expression  == max([1, 2, 3, 4]).expression == {
            "$max" : [1, 2, 3, 4]
        }

    def test_min(self)->None:
        """Tests $min operator class and mirror function"""


        min_op = Min(
            operand = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert min_op

        # Functional test
        # ---------------------
        assert min_op.expression  == min([1, 2, 3, 4]).expression == {
            "$min" : [1, 2, 3, 4]
        }


    def test_push(self)->None:
        """Tests the $push operator class and mirror function"""

        push_op = Push(
            operand = {
                "item" : "$item",
                "quantity" : "$quantity"
            }
        )

        # Unit test
        # -----------------
        assert push_op

        # Functional test
        # ---------------------
        assert push_op.expression == push({
                "item" : "$item",
                "quantity" : "$quantity"
            }).expression == {
                "$push" : {
                "item" : "$item",
                "quantity" : "$quantity"
                }
            }


    def test_sum(self)->None:
        """Tests $sum operator class and mirror function"""


        sum_op = Sum(
            operand = [1, 2, 3, {"$literal":4}]
        )

        # Unit test
        # ---------------------
        assert sum_op

        # Functional test
        # ---------------------
        assert sum_op.expression  == sum([1, 2, 3, {"$literal":4}]).expression == {
            "$sum" : [1, 2, 3, {"$literal":4}]
        }
