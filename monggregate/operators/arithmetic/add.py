"""
Module defining an interface to the $add operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/add/#mongodb-expression-exp.-add

Definition
-------------------
$add
Adds numbers together or adds numbers and a date. If one of the arguments is a date, 
$add treats the other arguments as milliseconds to add to the date.

The $add expression has the following syntax:

    >>> { $add: [ <expression1>, <expression2>, ... ] }

The arguments can be any valid expression 
as long as they resolve to either all numbers or to numbers and a date. For more information on expressions, see Expressions.

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Add(ArithmeticOperator):
    """
    Creates a $add expression

    Attributes
    -------------------
        - expressions, list[Any] : list of valid expressions,
                                   each expression must resolve to either 
                                   all numbers or to numbers and a date
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$add" : self.expressions
        })
    
def add(*args:Any)->Add:
    """Returns a $add operator"""

    return Add(
        expressions=list(args)
    )