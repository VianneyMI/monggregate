"""
Module defining an interface to MongoDB $sum accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 02/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sum/#mongodb-group-grp.-sum

"""

from pydantic import validator
from monggregate.expressions import Expression
from monggregate.operators.accumulators.accumulator import Accumulator

class Sum(Accumulator):
    """
    Creates a $sum expression.
    """

    operands : list[Expression] | None
    operand : Expression | None



    @validator("operand", pre=True, always=True)
    @classmethod
    def validate_operand(cls, operand:Expression|None, values:dict)->Expression|dict|None:
        """Valdidates and converts operand"""


        operands = values.get("operands")

        # Validation
        # --------------------------------------
        if not (operand or operands):
            raise ValueError("At least one of operand is required")


        if operand and operands:
            raise ValueError("Operand and Operands cannot be both set")


        return operand


    @property
    def statement(self) -> dict:

        return {
            "$sum" : self.operand or self.operands
        }

def sum(*args:Expression)->dict: # pylint: disable=redefined-builtin
    """Creates a $sum statement"""

    if len(args)>1:
        output = Sum(operands=list(args)).statement
    else:
        output = Sum(operand=args[0]).statement

    return output
