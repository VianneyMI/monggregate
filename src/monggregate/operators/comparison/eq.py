"""
Module defining an interface to MongoDB $eq operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/eq/#mongodb-expression-exp.-eq

Definition
-------------------
$eq
Compares two values and returns:

    * true when the values are equivalent.

    * false when the values are not equivalent.

The $eq compares both value and type, using the specified BSON comparison order for values of different types.

$eq has the following syntax:

    >>> { $eq: [ <expression1>, <expression2> ] }

The arguments can be any valid expression. For more information on expressions, see Expressions.


"""

from typing import Any
from monggregate.operators.comparison.comparator import Comparator

class Equal(Comparator):
    """
    Abstraction of MongoDB $eq operator which Compares two values and 
    returns true when the values are equivalent, False otherwise.

    Attributes
    -------------------
        - left, Any :Left operand. Can be any valid expression.
        - right, Any :Right operand. Can be any valid expression.

    Online MongoDB documentation
    ----------------------------
    Compares two values and returns:

        * true when the values are equivalent.

        * false when the values are not equivalent.

    The $eq compares both value and type, using the specified BSON comparison order for values of different types.

    $eq has the following syntax:

        >>> { $eq: [ <expression1>, <expression2> ] }

    The arguments can be any valid expression. For more information on expressions, see Expressions.
    
    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/eq/#mongodb-expression-exp.-eq)


    """

    @property
    def expression(self) -> dict:

        return self.express({
            "$eq":[self.left, self.right]
        })

Eq = Equal

def equal(left:Any, right:Any)->Equal:
    """Creates an $eq operator"""

    return Equal(
        left=left,
        right=right
    )

eq = equal
