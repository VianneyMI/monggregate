"""
Module defining an interface to MongoDB $cmp operator
"""

from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class Compare(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$cmp":[self.left, self.right]
        }

Cmp = Compare

def compare(left:Expression, right:Expression)->dict:
    """Returns a $cmp stament"""

    return Compare(
        left=left,
        right=right
    ).statement

cmp = compare