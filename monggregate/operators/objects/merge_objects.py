"""Module defining an interface to $mergeObjects operator"""

from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOperator

class MergeObjects(ArrayOperator):
    """Creates an $arrayToObject expression"""

    expression : Expression | list[Expression]


    @property
    def statement(self) -> dict:
        return {
            "$mergeObjects" : self.expression
        }

def merge_objects(expression:Expression)->dict:
    """Returns a merge_objects statement"""

    return MergeObjects(expression=expression).statement
