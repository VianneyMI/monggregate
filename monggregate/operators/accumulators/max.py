"""
Module defining an interface to MongoDB $max accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 06/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/max/#mongodb-group-grp.-max

"""

from pydantic import validator
from monggregate.expressions import Expression
from monggregate.operators.accumulators.accumulator import Accumulator

class Max(Accumulator):
    """
    Creates a $ max expression.
    """

    expression : Expression



    @property
    def statement(self) -> dict:

        return {
            "$max" : self.expression
        }

def max(expression:Expression)->dict:
    """Creates a push statement"""

    return Max(expression=expression).statement
