"""
Module defining an interface to MongoDB $lt operator
"""

from monggregate.operators.comparison.comparator import Comparator

class LowerThan(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$lt":[self.left, self.right]
        }

Lt = LowerThan
