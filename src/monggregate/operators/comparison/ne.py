"""
Module defining an interface to MongoDB $ne operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/ne/#mongodb-expression-exp.-ne

Definition
-------------------
$ne
Compares two values and returns:

    * true when the values are not equivalent.

    * false when the values are equivalent.

The $ne compares both value and type, using the specified BSON comparison order for values of different types.

$ne has the following syntax:

    >>> { $ne: [ <expression1>, <expression2> ] }

The arguments can be any valid expression. For more information on expressions, see Expressions.

"""

from typing import Any
from monggregate.base import Expression
from monggregate.operators.comparison.comparator import Comparator

class NotEqual(Comparator):
    """
    Abstraction of MongoDB $ne operator which compares two values and 
    returns true when the values are not equivalent, false otherwise.

    Attributes
    -------------------
        - left, Any :Left operand. Can be any valid expression.
        - right, Any :Right operand. Can be any valid expression.

    Online MongoDB documentation
    ----------------------------
    Compares two values and returns:

        * true when the values are not equivalent.

        * false when the values are equivalent.

    The $ne compares both value and type, using the specified BSON comparison order for values of different types.

    $ne has the following syntax:

        >>> { $ne: [ <expression1>, <expression2> ] }

    The arguments can be any valid expression. For more information on expressions, see Expressions.
    
    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/ne/#mongodb-expression-exp.-ne)
    """

    @property
    def expression(self) -> Expression:

        return self.express({
            "$ne":[self.left, self.right]
        })

Ne = NotEqual

def not_equal(left:Any, right:Any)->NotEqual:
    """Returns a $ne operator"""

    return NotEqual(
        left=left,
        right=right
    )

ne = not_equal
