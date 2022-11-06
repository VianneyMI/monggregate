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
    Creates a sum expression.
    """

    expression : Expression

    @validator("expression", pre=True, always=True)
    @classmethod
    def convert_expression(cls, expression : Expression)->Expression|dict:
        """Converts expression"""

        if isinstance(expression, Accumulator):
            output = expression.statement
        else:
            output = expression

        return output

    @property
    def statement(self) -> dict:

        return {
            "$push" : self.expression
        }

def first(expression:Expression)->dict:
    """Creates a push statement"""

    return First(expression=expression).statement
