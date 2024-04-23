"""
Module defining an interface to MongoDB $gt operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/gt/#mongodb-expression-exp.-gt

Definition
--------------------
$gt
Compares two values and returns:

    * true when the first value is greater than the second value.

    * false when the first value is less than or equivalent to the second value.

The $gt compares both value and type, using the specified BSON comparison order for values of different types.

$gt has the following syntax:

    >>> { $gt: [ <expression1>, <expression2> ] }

For more information on expressions, see Expressions.
"""

from typing import Any
from monggregate.base import Expression
from monggregate.operators.comparison.comparator import Comparator

class GreatherThan(Comparator):
    """
    Abstraction of MongoDB $gt operator which compares two values and 
    returns true when the first value is greater than the second value and false otherwise.

    Attributes
    -------------------
        - left, Any :Left operand. Can be any valid expression.
        - right, Any :Right operand. Can be any valid expression.

    Online MongoDB documentation
    ----------------------------
    Compares two values and returns:

        * true when the first value is greater than the second value.

        * false when the first value is less than or equivalent to the second value.

    The $gt compares both value and type, using the specified BSON comparison order for values of different types.

    $gt has the following syntax:

        >>> { $gt: [ <expression1>, <expression2> ] }

    For more information on expressions, see Expressions.
    
    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/gt/#mongodb-expression-exp.-gt)
    """

    @property
    def expression(self) -> Expression:

        return self.express({
            "$gt":[self.left, self.right]
        })

Gt = GreatherThan

def greather_than(left:Any, right:Any)->GreatherThan:
    """Returns a $gt operator"""

    return GreatherThan(
        left = left,
        right = right
        )

gt= greather_than