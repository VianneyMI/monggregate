"""
Module defining an interface to MongoDB $ne operator
"""

from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class NotEqual(Comparator):
    """Creates a $ne expression"""

    @property
    def statement(self) -> dict:

        return {
            "$ne":[self.left, self.right]
        }

Ne = NotEqual

def not_equal(left:Expression, right:Expression)->dict:
    """Returns a $ne statement"""

    return NotEqual(
        left=left,
        right=right
    ).statement

ne = not_equal
