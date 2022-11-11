"""Module gathering the tests of the boolean operators"""

# pylint: disable=import-error
import pytest
from monggregate.operators.boolean import(
    And, and_,
    Not, not_,
    Or, or_
)
from monggregate.operators.accumulators import First
from monggregate.operators.comparison import greather_than

@pytest.mark.operators
@pytest.mark.unit
@pytest.mark.functional
class TestBooleanOperators:
    """This class only aims at reusing the markers"""

    def test_and(self)->None:
        """Testes $and operator class and mirror function"""

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
        assert and_operator.statement == and_(First(expression=[1, 2, 3, 4]), First(expression=[4, 5, 6, 7])) == {
            "$and" : [
                {
                    "$first" : [1, 2, 3, 4]
                },
                {
                    "$first" : [4, 5, 6, 7]
                }
            ]
        }


    def test_not(self)->None:
        """Testes the $not operator class and mirror function"""

        not_op = Not(expression=greather_than("$qty", 250))

        # Unit test
        # --------------------
        assert not_op

        # Functional test
        # --------------------
        assert not_op.statement == not_(greather_than("$qty", 250)) == {
            "$not" : [{"$gt":["$qty", 250]}]
        }


    def test_or(self)->None:
        """Testes $or operator class and mirror function"""

        # Unit test
        # ---------------------------
        or_operator = Or(
            expressions=[
                First(expression=[1, 2, 3, 4]),
                First(expression=[4, 5, 6, 7])
            ]
        )

        assert or_operator

        # Functional tests
        # --------------------------
        assert or_operator.statement == or_(First(expression=[1, 2, 3, 4]), First(expression=[4, 5, 6, 7]))  == {
            "$or" : [
                {
                    "$first" : [1, 2, 3, 4]
                },
                {
                    "$first" : [4, 5, 6, 7]
                }
            ]
        }
