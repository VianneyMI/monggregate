"""
Module defining an interface to MongoDB $last accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 06/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/last/#mongodb-group-grp.-last

"""

from pydantic import validator
from monggregate.expressions import Expression
from monggregate.operators.accumulators.accumulator import Accumulator

class Last(Accumulator):
    """
    Creates a sum expression.
    """

    expression : Expression



    @property
    def statement(self) -> dict:

        return {
            "$last" : self.expression
        }

def last(expression:Expression)->dict:
    """Creates a push statement"""

    return Last(expression=expression).statement
