"""
Module defining an interface to $pow operator

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Pow(ArithmeticOperator):
    """
    xxx
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$add" : self.expressions
        })
    
def pow(*args:Any)->Pow:
    """Returns an $pow statement"""

    return Pow(
        expressions=list(args)
    )