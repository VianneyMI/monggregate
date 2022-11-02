"""Module defining an interface to $size operator"""

from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOnlyOperator

class Size(ArrayOnlyOperator):
    """Creates a $size expression"""

    @property
    def statement(self) -> dict:
        return {
            "$size":self.expression
        }

def size(array:Expression)->dict:
    """Returns a $size statement"""

    return Size(
        expression = array
    ).statement
