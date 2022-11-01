"""
Module defining an interface to MongoDB $gte operator
"""

from monggregate.operators.comparison.comparator import Comparator

class GreatherThanOrEqual(Comparator):
    """Creates a $gte expression"""

    @property
    def statement(self) -> dict:

        return {
            "$gte":[self.left, self.right]
        }

Gte = GreatherThanOrEqual
