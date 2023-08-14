"""
Module defining an interface to $switch operator

"""

from typing import Any
from monggregate.operators.conditional.conditional import ConditionalOperator

# TODO : Define branc <VM, 14/08/2023>
# {"case": <expression>, "then": <expression> }

class Switch(ConditionalOperator):
    """
    xxx
            
    
    """


    branches : list[Any]
    default : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$switch" : {
                "branches" : self.branches,
                "default" : self.default
            }
        })
    
def switch(branches:list[Any], default:Any)->Switch:
    """Returns an $switch statement"""

    return Switch(
        branches=branches,
        default=default
    )