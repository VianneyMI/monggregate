"""
Module defining an interface to $date_to_string operator

"""

from typing import Any
from monggregate.base import pyd
from monggregate.operators.strings.string import StringOperator

class DateToString(StringOperator):
    """
    xxx
            
    
    """


    date : Any
    format_ : Any = pyd.Field(alias="format")
    timezone : Any
    on_null : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$dateToString" : self.dict(by_alias=True, exclude_none=True)
        })
    
def date_to_string(
        date:Any,
        format_:Any=None,
        timezone:Any=None,
        on_null:Any=None
)->DateToString:
    """Returns an $dateToString statement"""

    return DateToString(
        date=date,
        format_=format_,
        timezone=timezone,
        on_null=on_null
    )