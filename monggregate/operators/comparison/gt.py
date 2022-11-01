"""
Module defining an interface to MongoDB $gt operator
"""

from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class GreatherThan(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$gt":[self.left, self.right]
        }

Gt = GreatherThan

def gt(left:Expression, right:Expression)->dict:

    return GreatherThan(
        left = left,
        right = right
        ).statement
