"""
Module defining an interface to the $dateToString operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/dateToString/#mongodb-expression-exp.-dateToString

Definition
-------------------
$dateToString
Converts a date object to a string according to a user-specified format.

The $dateToString expression has the following operator expression syntax:

    >>> { 
            $dateToString: {
                date: <dateExpression>,
                format: <formatString>,
                timezone: <tzExpression>,
                onNull: <expression>
            } 
        }

The $dateToString takes a document with the following fields:

Field                       Description
-------------------         -------------------

date                        Changed in version 3.6.
                            The date to convert to string. <dateExpression> must be a valid expression that resolves to a Date, a Timestamp, or an ObjectID.

format                      Optional. The date format specification. <formatString> can be any string literal, containing 0 or more format specifiers. 
                            For a list of specifiers available, see Format Specifiers.

                            If unspecified, $dateToString uses "%Y-%m-%dT%H:%M:%S.%LZ" as the default format.

timezone                    Optional. The timezone of the operation result. <tzExpression> must be a valid expression that resolves to a string formatted as either an 
                            Olson Timezone Identifier or a UTC Offset. If no timezone is provided, the result is displayed in UTC.

                            Format                              Examples
                            
                            Olson Timezone Identifier           "America/New_York"
                                                                "Europe/London"
                                                                "GMT"

                    
                            UTC Offset                          +/-[hh]:[mm], e.g. "+04:45"
                                                                +/-[hh][mm], e.g. "-0530"
                                                                +/-[hh], e.g. "+03"

onNull                      Optional. The value to return if the date is null or missing. The arguments can be any valid expression.
                            If unspecified, $dateToString returns null if the date is null or missing.

Format Specifiers
-------------------

Specifiers          Description                                     Possible Values

%d                  Day of Month (2 digits, zero padded)            01-31
%G                  Year in ISO 8601 format                         0000-9999
%H                  Hour (2 digits, zero padded, 24-hour clock)     00-23
%j                  Day of year (3 digits, zero padded)             001-366
%L                  Millisecond (3 digits, zero padded)             000-999
%m                  Month (2 digits, zero padded)                   01-12
%M                  Minute (2 digits, zero padded)                  00-59
%S                  Second (2 digits, zero padded)                  00-60
%w                  Day of week (1-Sunday, 7-Saturday)              1-7
%u                  Day of week number in ISO 8601 format 
                    (1-Monday, 7-Sunday)                            1-7
%U                  Week of year (2 digits, zero padded)            00-53
%V                  Week of Year in ISO 8601 format                 01-53
%Y                  Year (4 digits, zero padded)                    0000-9999
%z                  The timezone offset from UTC.                   +/-[hh][mm]
%Z                  The minutes offset from UTC as a number. 
                    For example, if the timezone offset 
                    (+/-[hhmm]) was +0445, 
                    the minutes offset is +285.                     +/-mmm
%%                  Percent Character as a Literal                  %



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
    """Returns an $dateToString operator"""

    return DateToString(
        date=date,
        format_=format_,
        timezone=timezone,
        on_null=on_null
    )