"""
Module defining an interface to MongoDB $gte operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/gte/#mongodb-expression-exp.-gte

$gte
Compares two values and returns:

    * true when the first value is greater than  or equivalent the second value.

    * false when the first value is less than to the second value.

The $gte compares both value and type, using the specified BSON comparison order for values of different types.

$gt has the following syntax:

    >>> { $gte: [ <expression1>, <expression2> ] }

For more information on expressions, see Expressions.
"""

from typing import Any
from monggregate.operators.comparison.comparator import Comparator

class GreatherThanOrEqual(Comparator):
    """
    Creates a $gte expression

    Attributes
    -------------------
        - left, Expression : Left operand. Can be any valid expression.
        - right, Expression : Right operand. Can be any valid expression.

    """

    @property
    def statement(self) -> dict:

        return self.resolve({
            "$gte":[self.left, self.right]
        })

Gte = GreatherThanOrEqual

def grether_than_or_equal(left:Any, right:Any)->GreatherThanOrEqual:
    """Returns a $gte operator"""

    return GreatherThanOrEqual(
        left=left,
        right=right
    )

gte = grether_than_or_equal
