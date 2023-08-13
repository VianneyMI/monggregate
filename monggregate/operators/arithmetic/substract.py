"""
Module defining an interface to $substract operator

"""

from typing import Any
from monggregate.operators.arithmetic.arithmetic import ArithmeticOperator

class Substract(ArithmeticOperator):
    """
    xxx
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$add" : self.expressions
        })
    
def substract(*args:Any)->Substract:
    """Returns an $substract statement"""

    return Substract(
        expressions=list(args)
    )