"""
Module defining an interface to $millisecond operator

"""

from typing import Any
from monggregate.operators.date.date import DateOperator

class MilliSecond(DateOperator):
    """
    xxx
            
    
    """


    expression : Any
    timezeone : Any | None

    @property
    def statement(self) -> dict:

        if self.timezeone:
            inner = {
                "date" : self.expression,
                "timezone" : self.timezeone
            }
        else:
            inner = self.expression

        return self.resolve({
            "$millisecond" : inner
        })
    
def millisecond(expression:Any, timezone:Any)->MilliSecond:
    """Returns an $millisecond statement"""

    return MilliSecond(
        expression=expression,
        timezone=timezone
    )