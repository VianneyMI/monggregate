"""
Module defining an interface to $multiply operator

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Multiply(ArithmeticOperator):
    """
    xxx
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$multiply" : self.expressions
        })
    
def multiply(*args:Any)->Multiply:
    """Returns an $multiply statement"""

    return Multiply(
        expressions=list(args)
    )