"""Module defining an interface to $last operator"""

from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOnlyOperator

class Last(ArrayOnlyOperator):
    """Creates a $last expression"""

    @property
    def statement(self) -> dict:
        return {
            "$last":self.expression
        }

def last(array:Expression)->dict:
    """Returns a $last statement"""

    return Last(
        expression = array
    ).statement
