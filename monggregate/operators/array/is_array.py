"""Module defining an interface to $isArray operator"""

from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOnlyOperator

class IsArray(ArrayOnlyOperator):
    """Creates a $isArray expression"""

    @property
    def statement(self) -> dict:
        return {
            "$isArray":self.expression
        }

def is_array(array:Expression)->dict:
    """Returns a $isArray statement"""

    return IsArray(
        expression = array
    ).statement
