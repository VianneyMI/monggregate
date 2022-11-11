"""Module defining an interface to $mergeObjects operator"""

from monggregate.operators.array.array import ArrayOperator
from monggregate.expressions import Expression

class ObjectToArray(ArrayOperator):
    """Creates an $arrayToObject expression"""

    expression : Expression

    @property
    def statement(self) -> dict:
        return {
            "$objectToArray" : self.expression
        }

def object_to_array(expression:Expression)->dict:
    """Returns a *objectToArray statement"""

    return ObjectToArray(expression=expression).statement
