"""
Module defining an interface to MongoDB $lt operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/lt/#mongodb-expression-exp.-lt

$lt
Compares two values and returns:

    * true when the first value is less than the second value.

    * false when the first value is greater than or equivalent to the second value.

The $gt compares both value and type, using the specified BSON comparison order for values of different types.

$lt has the following syntax:

    >>> { $lt: [ <expression1>, <expression2> ] }

For more information on expressions, see Expressions.
"""

from typing import Any
from monggregate.operators.comparison.comparator import Comparator

class LowerThan(Comparator):
    """
    Creates a $lt expression

    Attributes
    -------------------
        - left, Expression : Left operand. Can be any valid expression.
        - right, Expression : Right operand. Can be any valid expression.
    """

    @property
    def statement(self) -> dict:

        return self.resolve({
            "$lt":[self.left, self.right]
        })

Lt = LowerThan

def lower_than(left:Any, right:Any)->LowerThan:
    """Returns a $lt operator"""

    return LowerThan(
        left=left,
        right=right
    )

lt = lower_than
