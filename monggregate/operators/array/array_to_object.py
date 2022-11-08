"""Module defining an interface to $arrayToObject operator"""

from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOperator

class ArrayToObject(ArrayOperator):
    """Creates an $arrayToObject expression"""

    expression : Expression


    @property
    def statement(self) -> dict:
        return {
            "$arrayToObject" : self.expression
        }

def array_to_object(expression:Expression)->dict:
    """Returns an $arrayToObject statement"""

    return ArrayToObject(expression=expression).statement
