"""
Module defining an interface to MongoDB $cmp operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/cmp/#mongodb-expression-exp.-cmp

Definition
--------------------
$cmp
Compares two values and returns:

    * -1 if the first value is less than the second.

    * 1 if the first value is greater than the second.

    * 0 if the two values are equivalent.

The $cmp compares both value and type, using the specified BSON comparison order for values of different types.

$cmp has the following syntax:

    >>> { $cmp: [ <expression1>, <expression2> ] }

For more information on expressions, see Expressions.

"""

from typing import Any
from monggregate.operators.comparison.comparator import Comparator

class Compare(Comparator):
    """
    Creates a $cmp expression

    Attributes
    -------------------
        - left, Expression : Left operand. Can be any valid expression.
        - right, Expression : Right operand. Can be any valid expression.

    """

    @property
    def statement(self) -> dict:

        return self.resolve({
            "$cmp":[self.left, self.right]
        })

Cmp = Compare

def compare(left:Any, right:Any)->Compare:
    """Returns a $cmp stament"""

    return Compare(
        left=left,
        right=right
    )

cmp = compare