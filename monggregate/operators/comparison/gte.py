"""
Module defining an interface to MongoDB $gte operator
"""

from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class GreatherThanOrEqual(Comparator):
    """Creates a $gte expression"""

    @property
    def statement(self) -> dict:

        return {
            "$gte":[self.left, self.right]
        }

Gte = GreatherThanOrEqual

def grether_than_or_equal(left:Expression, right:Expression)->dict:
    """Returns a $gte statement"""

    return GreatherThanOrEqual(
        left=left,
        right=right
    ).statement

gte = grether_than_or_equal
