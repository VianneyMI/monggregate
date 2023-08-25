"""
Module defining an interface to the $multiply operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/multiply/#mongodb-expression-exp.-multiply

Definition
-------------------
$multiply
Multiplies numbers together and returns the result. Pass the arguments to 
$multiply in an array.

The $multiply expression has the following syntax:

    >>> { $multiply: [ <expression1>, <expression2>] }

The arguments can be any valid expression as long as they resolve to numbers. 
For more information on expressions, see Expressions.

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Multiply(ArithmeticOperator):
    """
    Creates a $multiply expression

    Attributes
    -------------------
        - expressions, list[Any] : list of valid expressions
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$multiply" : self.expressions
        })
    
def multiply(*args:Any)->Multiply:
    """Returns a $multiply operator"""

    return Multiply(
        expressions=list(args)
    )