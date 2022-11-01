"""
Module defining an interface to MongoDB $cmp operator
"""

from monggregate.operators.comparison.comparator import Comparator

class Compare(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$cmp":[self.left, self.right]
        }

Cmp = Compare
