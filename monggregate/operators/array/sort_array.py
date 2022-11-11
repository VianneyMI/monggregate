"""Module defining an interface to $maxn operator"""

from typing import Literal
from pydantic import Field
from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOperator

class SortArray(ArrayOperator):
    """Creates a $first expression"""

    expression : Expression = Field(alias="input")
    by : dict[str, Literal[1, -1]] = Field(1, alias="sort_by")

    @property
    def statement(self) -> dict:
        return {
            "$sortArray":{
                "input" : self.expression,
                "sortBy" : self.by
            }
        }

def sort_array(expression:Expression, sort_by:dict[str, Literal[1, -1]])->dict:
    """Returns a $first statement"""

    return SortArray(
        expression = expression,
        sort_by = sort_by
    ).statement
