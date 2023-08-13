"""
Module defining an interface to $divide operator

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Divide(ArithmeticOperator):
    """
    xxx
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$add" : self.expressions
        })
    
def divide(*args:Any)->Divide:
    """Returns an $divide statement"""

    return Divide(
        expressions=list(args)
    )