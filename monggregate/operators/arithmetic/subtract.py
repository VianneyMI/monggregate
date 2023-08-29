"""
Module defining an interface to the $substract operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/substract/#mongodb-expression-exp.-substract

Definition
-------------------
$substract
Subtracts two numbers to return the difference, or two dates to return the difference in milliseconds, 
or a date and a number in milliseconds to return the resulting date.

The $substract expression has the following syntax:

    >>> { $substract: [ <expression1>, <expression2>] }

The second argument is subtracted from the first argument.

The arguments can be any valid expression as long as they resolve to numbers and/or dates. To subtract a number from a date, the date must be the first argument. 
For more information on expressions, see Expressions.

Behavior
-------------------

Starting in MongoDB 5.0, the result will have the same type as the input except when it cannot be represented accurately in that type. In these cases:

    * A 32-bit integer will be converted to a 64-bit integer if the result is representable as a 64-bit integer.

    * A 32-bit integer will be converted to a double if the result is not representable as a 64-bit integer.

    * A 64-bit integer will be converted to double if the result is not representable as a 64-bit integer.



"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Subtract(ArithmeticOperator):
    """
    Creates a $substract expression

    Attributes
    -------------------
        - left, Any : the numerator of the division
        - right, Any : the denominator of the division
            
    
    """


    left: Any
    right: Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$substract" : [self.left, self.right]
        })
    
def subtract(left:Any, right:Any)->Subtract:
    """Returns a $substract operator"""

    return Subtract(
        left=left,
        right=right
    )