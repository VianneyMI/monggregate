"""
Module defining an interface to $millisecond operator

"""

from typing import Any
from monggregate.operators.date.date import DateOperator

class Millisecond(DateOperator):
    """
    Creates a $millisecond expression

    Attributes
    -------------------
        - expression, Any : the expression that must resolve to a date
        - timezone, Any | None : the timezone to use for the date
            
    
    """


    expression : Any
    timezone : Any | None

    @property
    def statement(self) -> dict:

        if self.timezone:
            inner = {
                "date" : self.expression,
                "timezone" : self.timezone
            }
        else:
            inner = self.expression

        return self.resolve({
            "$millisecond" : inner
        })
    
def millisecond(expression:Any, timezone:Any)->Millisecond:
    """Returns an $millisecond operator"""

    return Millisecond(
        expression=expression,
        timezone=timezone
    )