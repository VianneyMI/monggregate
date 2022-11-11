"""Module defining an interface to $maxn operator"""

from pydantic import Field
from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOperator

class MaxN(ArrayOperator):
    """Creates a $maxN expression"""

    expression : Expression = Field(alias="input")
    limit : Expression = Field(1, alias="n")

    @property
    def statement(self) -> dict:
        return {
            "$maxN" : {
                "n" : self.limit,
                "input" : self.expression
            }
        }

def max_n(expression:Expression, limit:Expression=1)->dict:
    """Returns a $maxN statement"""

    return MaxN(
        expression = expression,
        limit = limit
    ).statement
