"""
Module defining an interface to $concat operator

"""

from typing import Any
from monggregate.operators.strings.string import StringOperator

class Concat(StringOperator):
    """
    xxx
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$concat" : self.expressions
        })
    
def concat(*args:Any)->Concat:
    """Returns an $concat statement"""

    return Concat(
        expressions=list(args)
    )