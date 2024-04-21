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
        """Tests $and operator class and mirror function"""

        # Unit test
        # ---------------------------
        and_operator =  And(
            operands=[
                First(operand=[1, 2, 3, 4]),
                First(operand=[4, 5, 6, 7])
            ]
        )

        assert and_operator

        # Functional tests
        # --------------------------
        assert and_operator.operand == and_(First(operand=[1, 2, 3, 4]), First(operand=[4, 5, 6, 7])).operand == {
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
        """Tests the $not operator class and mirror function"""

        not_op = Not(operand=greather_than("$qty", 250))

        # Unit test
        # --------------------
        assert not_op

        # Functional test
        # --------------------
        assert not_op.operand == not_(greather_than("$qty", 250)).operand == {
            "$not" : [{"$gt":["$qty", 250]}]
        }


    def test_or(self)->None:
        """Tests $or operator class and mirror function"""

        # Unit test
        # ---------------------------
        or_operator = Or(
            operands=[
                First(operand=[1, 2, 3, 4]),
                First(operand=[4, 5, 6, 7])
            ]
        )

        assert or_operator

        # Functional tests
        # --------------------------
        assert or_operator.operand == or_(First(operand=[1, 2, 3, 4]), First(operand=[4, 5, 6, 7])).operand  == {
            "$or" : [
                {
                    "$first" : [1, 2, 3, 4]
                },
                {
                    "$first" : [4, 5, 6, 7]
                }
            ]
        }
