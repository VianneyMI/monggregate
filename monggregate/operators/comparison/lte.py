"""
Module defining an interface to MongoDB $lte operator
"""

from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class LowerThanOrEqual(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$lte":[self.left, self.right]
        }

Lte = LowerThanOrEqual

def lower_than_or_equal(left:Expression, right:Expression)->dict:
    """Returns a $lt statement"""

    return LowerThanOrEqual(
        left=left,
        right=right
    ).statement

lte = lower_than_or_equal
