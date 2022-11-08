"""Module defining an interface to $or operator"""

from monggregate.expressions import Expression
from monggregate.operators.boolean.boolean import BooleanOperator

class Or(BooleanOperator):
    """Creates a $or expression"""

    expressions : list[Expression]

    # TODO : Add validator to convert expressions

    @property
    def statement(self) -> dict:
        return {
            "$or" : self.expressions
        }

def or_(*args:Expression)->dict:
    """Returns an $or statement"""

    return Or(
        expressions=args
    ).statement
