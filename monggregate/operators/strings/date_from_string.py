"""
Module defining an interface to $date_from_string operator

"""

from typing import Any
from monggregate.base import pyd
from monggregate.operators.strings.string import StringOperator

class DateFromString(StringOperator):
    """
    xxx
            
    
    """


    date_string : Any
    format_ : Any = pyd.Field(alias="format")
    timezone : Any
    on_error : Any
    on_null : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$dateFromString" : self.dict(by_alias=True, exclude_none=True)
        })
    
def date_from_string(
        date_string:Any,
        format_:Any=None,
        timezone:Any=None,
        on_error:Any=None,
        on_null:Any=None
)->DateFromString:
    """Returns an $dateFromString statement"""

    return DateFromString(
        date_string=date_string,
        format_=format_,
        timezone=timezone,
        on_error=on_error,
        on_null=on_null
    )