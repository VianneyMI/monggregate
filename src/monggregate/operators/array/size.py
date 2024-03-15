"""
Module defining an interface to $size operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------

Last Updated (in this package) : 12/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/size/#mongodb-expression-exp.-size

Definition
---------------------------
$size
Counts and returns the total number of items in an array.

$size has the following syntax:

    >>> { $size: <expression> }

The argument for $size can be any expression as long as it resolves to an array.
For more information on expressions, see Expressions.

Behavior
----------------------------
The argument for $size must resolve to an array.
If the argument for $size is missing or does not resolve to an array,
$size errors.

"""

from typing import Any
from monggregate.operators.array.array import ArrayOnlyOperator

class Size(ArrayOnlyOperator):
    """
    Creates a $size expression

    Attributes
    --------------------
        - expression : Any valid expression that resolves to an array

    """

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$size":self.expression
        })

def size(array:Any)->Size:
    """Returns a $size operator"""

    return Size(
        expression = array
    )
