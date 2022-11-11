"""Module defining an interface to $minn operator"""

from pydantic import Field
from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOperator

class MinN(ArrayOperator):
    """Creates a $minN expression"""

    expression : Expression = Field(alias="input")
    limit : Expression = Field(1, alias="n")

    @property
    def statement(self) -> dict:
        return {
            "$minN" : {
                "n" : self.limit,
                "input" : self.expression
            }
        }

def min_n(expression:Expression, limit:Expression=1)->dict:
    """Returns a $minN statement"""

    return MinN(
        expression = expression,
        limit = limit
    ).statement
