"""Module defining an interface to $and operator"""

from monggregate.expressions import Expression
from monggregate.operators.boolean.boolean import BooleanOperator

class And(BooleanOperator):
    """Creates a $or expression"""

    expressions : list[Expression]

    # TODO : Add validator to convert expressions

    @property
    def statement(self) -> dict:
        return {
            "$and" : self.expressions
        }

def and_(*args:Expression)->dict:
    """Returns an $and statement"""

    return And(
        expressions=list(args)
    ).statement
