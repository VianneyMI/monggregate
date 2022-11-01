"""
Module defining an interface to MongoDB $eq operator
"""

from monggregate.operators.comparison.comparator import Comparator

class Equal(Comparator):
    """Creates a $gt expression"""

    @property
    def statement(self) -> dict:

        return {
            "$eq":[self.left, self.right]
        }

Eq = Equal
