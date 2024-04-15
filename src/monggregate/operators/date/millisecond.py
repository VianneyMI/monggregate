"""
Module defining an interface to $millisecond operator

"""

from typing import Any
from monggregate.operators.date.date import DateOperator

class Millisecond(DateOperator):
    """
    Abstraction of MongoDB $millisecond operator which returns the 
    millisecond portion of a date as an integer between 0 and 999.

    Attributes
    -------------------
        - expression, Any : the expression that must resolve to a date
        - timezone, Any | None : the timezone to use for the date
            
    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/millisecond)
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