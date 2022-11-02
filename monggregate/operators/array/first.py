"""Module defining an interface to $first operator"""

from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOnlyOperator

class First(ArrayOnlyOperator):
    """Creates a $first expression"""

    @property
    def statement(self) -> dict:
        return {
            "$first":self.expression
        }

def first(array:Expression)->dict:
    """Returns a $first statement"""

    return First(
        expression = array
    ).statement
