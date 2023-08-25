"""
Module defining an interface to the $divide operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/divide/#mongodb-expression-exp.-divide

Definition
-------------------
$divide
Divides one number by another and returns the result. Pass the arguments to 
$divide in an array.

The $divide expression has the following syntax:

    >>> { $divide: [ <expression1>, <expression2>] }

The first argument is the dividend, and the second argument is the divisor; i.e. the first argument is divided by the second argument.

The arguments can be any valid expression as long as they resolve to numbers. For more information on expressions, see Expressions.

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Divide(ArithmeticOperator):
    """
    Creates a $divide expression

    Attributes
    -------------------
        - numerator, Any : the numerator of the division
        - denominator, Any : the denominator of the division
            
    
    """


    numerator : Any
    denominator : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$divide" : [self.numerator, self.denominator]
        })
    
def divide(numerator:Any, denominator:Any)->Divide:
    """Returns a $divide operator"""

    return Divide(
        numerator=numerator,
        denominator=denominator
    )
