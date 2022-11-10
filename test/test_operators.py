"""
Module unit testing the stages.

Checks that at least each stage can be instantiated properly.

"""

import pytest
from pydantic import ValidationError

from monggregate.operators import( # pylint: disable=import-error
    And, and_,
    Average, average,
    GreatherThan, greather_than,
    Sum, sum,
    Filter, filter,
    First, first,
    Last, last,
    Min, min,
    Max, max,
    Push, push,
)

# TODO : Group those test in a class to avoid having to duplicate the marks
# ----------------------
# Units Tests
# ----------------------
@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_and()->None:
    """Testes $and operator"""

    # Unit test
    # ---------------------------
    and_operator =  And(
        expressions=[
            First(expression=[1, 2, 3, 4]),
            First(expression=[4, 5, 6, 7])
        ]
    )

    assert and_operator

    # Functional tests
    # --------------------------
    assert and_operator.statement == {
        "$and" : [
            {
                "$first" : [1, 2, 3, 4]
            },
            {
                "$first" : [4, 5, 6, 7]
            }
        ]
    }

    # the mirror function should return the same statement than the class
    assert and_operator.statement == and_(First(expression=[1, 2, 3, 4]), First(expression=[4, 5, 6, 7]))

@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_average()->None:
    """Testes $avg operator"""


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


@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_sum()->None:
    """Testes $avg operator"""


    sum_op = Sum(
        operands = [1, 2, 3, 4]
    )

    # Unit test
    # ---------------------
    assert sum_op

    # Functional test
    # ---------------------
    assert sum_op.statement  == sum([1, 2, 3, 4]) == {
        "$sum" : [1, 2, 3, 4]
    }


@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_last()->None:
    """Testes $avg operator"""


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


@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_first()->None:
    """Testes $first operator"""


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


@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_max()->None:
    """Testes $max operator"""


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

@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_min()->None:
    """Testes $min operator"""


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

@pytest.mark.operator
@pytest.mark.unit
@pytest.mark.functional
def test_filter()->None:
    """Testes $filter operator"""


    filter_op = Filter(
        array = [1, 2, 3, 4],
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
        ) == {
        "$filter" : {
            "input" : [1, 2, 3, 4],
            "as" : "num",
            "cond" : {
                "$gt" : ["$$num", 2]
            },
            "limit":None
        }
    }


if __name__ == "__main__":
    test_and()
