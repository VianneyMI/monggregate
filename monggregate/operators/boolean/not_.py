"""Module defining an interface to $not operator"""

from monggregate.expressions import Expression
from monggregate.operators.boolean.boolean import BooleanOperator

class Not(BooleanOperator):
    """Creates a $or expression"""

    expression : Expression

    # TODO : Add validator to convert expressions

    @property
    def statement(self) -> dict:
        return {
            "$not" : self.expression
        }

def not_(expression:Expression)->dict:
    """Returns an $not statement"""

    return Not(
        expression=expression
    ).statement
