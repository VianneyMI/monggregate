"""
Module defining an interface to $isArray operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------

Last Updated (in this package) : 12/11/2022
Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/isArray/#mongodb-expression-exp.-isArray

Definition
--------------------------
$isArray
Determines if the operand is an array. Returns a boolean.

$isArray has the following syntax:
    >>> { $isArray: [ <expression> ] }

Behavior
-----------------------------
The <expression> can be any valid expression. For more information on expressions, see Expressions.

NOTE : Aggregation expressions accept a variable number of arguments. These arguments are normally passed as an array.
       However, when the argument is a single value,
       you can simplify your code by passing the argument directly without wrapping it in an array.

"""

from typing import Any
from monggregate.operators.array.array import ArrayOnlyOperator

class IsArray(ArrayOnlyOperator):
    """
    Creates a $isArray expression

    Attributes
    -------------------------
        - expression : Any valid expression

    """

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$isArray":self.expression
        })

def is_array(array:Any)->IsArray:
    """Returns a $isArray operator"""

    return IsArray(
        expression = array
    )
