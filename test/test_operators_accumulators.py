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
        """Testes the $avg operator class and mirror function"""

        average_op = Average(
        expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert average_op

        # Functional test
        # ---------------------
        assert average_op.statement  == average([1, 2, 3, 4]) == {
            "$avg" : [1, 2, 3, 4]
        }

    def test_count(self)->None:
        """Testes the $count operator class and mirror function"""

        count_op = Count()

        # Unit test
        # ---------------------
        assert count_op

        # Functional test
        # ---------------------
        assert count_op.statement  == count() == {
            "$count" : {}
        }



    def test_first(self)->None:
        """Testes $first operator class and mirror function"""


        first_op = First(
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert first_op

        # Functional test
        # ---------------------
        assert first_op.statement  == first([1, 2, 3, 4]) == {
            "$first" : [1, 2, 3, 4]
        }


    def test_last(self)->None:
        """Testes $last operator class and mirror function"""


        last_op = Last(
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert last_op

        # Functional test
        # ---------------------
        assert last_op.statement  == last([1, 2, 3, 4]) == {
            "$last" : [1, 2, 3, 4]
        }

    def test_max(self)->None:
        """Testes $max operator class and mirror function"""


        max_op = Max(
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert max_op

        # Functional test
        # ---------------------
        assert max_op.statement  == max([1, 2, 3, 4]) == {
            "$max" : [1, 2, 3, 4]
        }

    def test_min(self)->None:
        """Testes $min operator class and mirror function"""


        min_op = Min(
            expression = [1, 2, 3, 4]
        )

        # Unit test
        # ---------------------
        assert min_op

        # Functional test
        # ---------------------
        assert min_op.statement  == min([1, 2, 3, 4]) == {
            "$min" : [1, 2, 3, 4]
        }


    def test_push(self)->None:
        """Testes the $push operator class and mirror function"""

        push_op = Push(
            expression = {
                "item" : "$item",
                "quantity" : "$quantity"
            }
        )

        # Unit test
        # -----------------
        assert push_op

        # Functional test
        # ---------------------
        assert push_op.statement == push({
                "item" : "$item",
                "quantity" : "$quantity"
            }) == {
                "$push" : {
                "item" : "$item",
                "quantity" : "$quantity"
                }
            }


    def test_sum(self)->None:
        """Testes $sum operator class and mirror function"""


        sum_op = Sum(
            expression = [1, 2, 3, {"$literal":4}]
        )

        # Unit test
        # ---------------------
        assert sum_op

        # Functional test
        # ---------------------
        assert sum_op.statement  == sum([1, 2, 3, {"$literal":4}]) == {
            "$sum" : [1, 2, 3, {"$literal":4}]
        }
