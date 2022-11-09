"""
Module defining an interface to MongoDB $first accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 06/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/first/#mongodb-group-grp.-first

"""

from pydantic import validator
from monggregate.expressions import Expression
from monggregate.operators.accumulators.accumulator import Accumulator

class First(Accumulator):
    """
    Creates a $first expression.
    """

    expression : Expression


    @property
    def statement(self) -> dict:

        return {
            "$first" : self.expression
        }

def first(expression:Expression)->dict:
    """Creates a push statement"""

    return First(expression=expression).statement
