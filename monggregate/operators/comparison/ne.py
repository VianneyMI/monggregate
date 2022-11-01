"""
Module defining an interface to MongoDB $ne operator
"""

from monggregate.operators.comparison.comparator import Comparator

class NotEqual(Comparator):
    """Creates a $ne expression"""

    @property
    def statement(self) -> dict:

        return {
            "$ne":[self.left, self.right]
        }

Ne = NotEqual
