"""
Module defining an interface to MongoDB $avg accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 06/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/avg/#mongodb-group-grp.-avg

"""


from monggregate.expressions import Expression
from monggregate.operators.accumulators.accumulator import Accumulator

class Average(Accumulator):
    """
    Creates a sum expression.
    """

    expression : Expression

    @property
    def statement(self) -> dict:

        return {
            "$avg" : self.expression
        }
Avg = Average

def average(expression:Expression)->dict:
    """Creates a push statement"""

    return Average(expression=expression).statement

avg = average
