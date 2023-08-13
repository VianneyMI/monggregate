"""
Module defining an interface to $and operator

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Add(ArithmeticOperator):
    """
    Creates a $add expression

    Attributes
    -------------------
        - expressions : list[Any]
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$add" : self.expressions
        })
    
def add(*args:Any)->Add:
    """Returns an $add statement"""

    return Add(
        expressions=list(args)
    )