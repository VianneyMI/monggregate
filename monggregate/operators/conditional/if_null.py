"""
Module defining an interface to $if_null operator

"""

from typing import Any
from monggregate.operators.conditional.conditional import ConditionalOperator

class IfNull(ConditionalOperator):
    """
    xxx
            
    
    """


    expression : Any # NOTE : Maybe diverge from Mongo and do not allow multiple expressions <VM, 14/08/2023>
    output : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$ifNull" : [self.expression, self.output]
        })
    
def if_null(expression:Any, output:Any)->IfNull:
    """Returns an $if_null statement"""

    return IfNull(
        expression=expression,
        output=output
    )