"""
Module defining an interface to MongoDB $lte operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/lte/#mongodb-expression-exp.-lte

$lt
Compares two values and returns:

    * true when the first value is less than or equivalent the second value.

    * false when the first value is greater than or equivalent to the second value.

The $gt compares both value and type, using the specified BSON comparison order for values of different types.

$lt has the following syntax:

    >>> { $lt: [ <expression1>, <expression2> ] }

For more information on expressions, see Expressions.
"""

from typing import Any
from monggregate.operators.comparison.comparator import Comparator

class LowerThanOrEqual(Comparator):
    """
    Creates a $gt expression.

    Attributes
    -------------------
        - left, Expression : Left operand. Can be any valid expression.
        - right, Expression : Right operand. Can be any valid expression.

    """

    @property
    def statement(self) -> dict:

        return self.resolve({
            "$lte":[self.left, self.right]
        })

Lte = LowerThanOrEqual

def lower_than_or_equal(left:Any, right:Any)->LowerThanOrEqual:
    """Returns a $lt operator"""

    return LowerThanOrEqual(
        left=left,
        right=right
    )

lte = lower_than_or_equal
