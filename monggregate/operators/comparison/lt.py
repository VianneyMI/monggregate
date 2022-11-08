"""
Module defining an interface to MongoDB $lt operator
"""

from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class LowerThan(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$lt":[self.left, self.right]
        }

Lt = LowerThan

def lower_than(left:Expression, right:Expression)->dict:
    """Returns a $lt statement"""

    return LowerThan(
        left=left,
        right=right
    ).statement

lt = lower_than
