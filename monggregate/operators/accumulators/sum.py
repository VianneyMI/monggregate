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
    Creates a sum expression.
    """

    operands : list[Expression] | None
    operand : Expression | None

    @validator("operands", pre=True, always=True)
    @classmethod
    def convert_operands(cls, operands:list[Expression]|None)->list|None:
        """Converts operands"""

        output = []
        if isinstance(operands, list):
            for operand in operands:
                # TODO : Replace accumulator by parent ancestor of stages and operators.
                if isinstance(operand, Accumulator):
                    output.append(operand.statement)
                else:
                    output.append(operand)
        else:
            output = operands

        return output

    @validator("operand", pre=True, always=True)
    @classmethod
    def convert_operand(cls, operand:Expression|None, values:dict)->Expression|dict|None:
        """Valdidates and converts operand"""


        operands = values.get("operands")

        # Validation
        # --------------------------------------
        if not (operand or operands):
            raise ValueError("At least one of operand is required")


        if operand and operands:
            raise ValueError("Operand and Operands cannot be both set")

        # Conversion
        # ---------------------------------------
        if isinstance(operand, Accumulator):
            output = operand.statement
        else:
            output = operand

        return output


    @property
    def statement(self) -> dict:

        return {
            "$sum" : self.operand or self.operands
        }
