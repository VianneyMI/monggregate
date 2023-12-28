"""
Module defining an interface to $not operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/not/#mongodb-expression-exp.-not

Definition
---------------
$not
Evaluates a boolean and returns the opposite boolean value; i.e. when passed an expression that evaluates to true,
$not returns false; when passed an expression that evaluates to false, $not returns true.

$not has the following syntax:

    >>> { $not: [ <expression> ] }

For more information on expressions, see Expressions.

Behavior
---------------
In addition to the false boolean value,
$not evaluates as false the following: null, 0, and undefined values.
The $not evaluates all other values as true, including non-zero numeric values and arrays.

"""

from typing import Any
from monggregate.operators.boolean.boolean import BooleanOperator

class Not(BooleanOperator):
    """
    Creates a $or expression

    Attributes
    -------------------
        - expression, Expression : Any valid expression

    """

    expression : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$not" : [self.expression]
        })

def not_(expression:Any)->Not:
    """Returns a $not operator"""

    return Not(
        expression=expression
    )
