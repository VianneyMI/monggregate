"""Module defining an interface to $inoperator"""

from pydantic import Field
from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOperator

class In(ArrayOperator):
    """Creates a $maxN expression"""

    expression : Expression = Field(1, alias="n")
    array : Expression = Field(alias="input")


    @property
    def statement(self) -> dict:
        return {
            "$in":[self.expression, self.array]
        }

def in_(expression:Expression, array:Expression)->dict:
    """Returns a $maxN statement"""

    return In(
        expression = expression,
        array = array
    ).statement
