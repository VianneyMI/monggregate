"""
Module defining an interface to MongoDB $eq operator
"""

from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class Equal(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$eq":[self.left, self.right]
        }

Eq = Equal

def equal(left:Expression, right:Expression)->dict:
    """Creates an $eq statement"""

    return Equal(
        left=left,
        right=right
    ).statement

eq = equal
