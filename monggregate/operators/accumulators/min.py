"""
Module defining an interface to MongoDB $min accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 06/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/min/#mongodb-group-grp.-min

"""

from pydantic import validator
from monggregate.expressions import Expression
from monggregate.operators.accumulators.accumulator import Accumulator

class Min(Accumulator):
    """
    Creates a $min expression.
    """

    expression : Expression



    @property
    def statement(self) -> dict:

        return {
            "$min" : self.expression
        }

def min(expression:Expression)->dict:
    """Creates a $min statement"""

    return Min(expression=expression).statement
