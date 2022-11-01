"""
Module defining an interface to MongoDB $lte operator
"""

from monggregate.operators.comparison.comparator import Comparator

class LowerThanOrEqual(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$lte":[self.left, self.right]
        }

Lt = LowerThanOrEqual
