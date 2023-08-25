"""
Module defining an interface to the $dateFromString operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/dateFromString/#mongodb-expression-exp.-dateFromString

Definition
-------------------
$dateFromString
Converts a date/time string to a date object.

The $dateFromString expression has the following syntax:

    >>> { 
            $dateFromString: { 
                dateString: <dateStringExpression>, 
                format: <formatStringExpression>, 
                timezone: <tzExpression>, 
                onError: <onErrorExpression>, 
                onNull: <onNullExpression> 
                } 
        }

The $dateFromString takes a document with the following fields:


Field                   Description
-------------------     -------------------
dateString              The date/time string to convert to a date object. See Date for more information on date/time formats.
                        NOTE: If specifying the timezone option to the operator, do not include time zone information in the dateString.

format                  Optional. The date format specification of the dateString. The format can be any expression that evaluates to a string literal, containing 0 or more format specifiers. 
                        For a list of specifiers available, see Format Specifiers.
                        If unspecified, $dateFromString uses "%Y-%m-%dT%H:%M:%S.%LZ" as the default format but accepts a variety of formats and attempts to parse the dateString if possible.

timezone                Optional. The time zone to use to format the date.
                        NOTE: If the dateString argument is formatted like '2017-02-08T12:10:40.787Z', in which the 'Z' at the end indicates Zulu time (UTC time zone), you cannot specify the timezone argument.

onError                 Optional.  If $dateFromString encounters an error while parsing the given dateString, it outputs the result value of the provided onError expression. 
                        This result value can be of any type.

                        If you do not specify onError, $dateFromString throws an error if it cannot parse dateString.

onNull                  Optional. If the dateString provided to $dateFromString is null or missing, it outputs the result value of the provided onNull expression. 
                        This result value can be of any type.
                        If you do not specify onNull and dateString is null or missing, then $dateFromString outputs null.

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

class DateFromString(StringOperator):
    """
    Creates a $concat expression

    Attributes
    -------------------
        - date_string, Any : the date/time string to convert to a date object. See Date for more information on date/time formats.
        - format_, Any : Optional. The date format specification of the dateString. The format can be any expression that evaluates to a string literal, containing 0 or more format specifiers.
        - timezone, Any : Optional. The time zone to use to format the date.
        - on_error, Any : Optional.  If $dateFromString encounters an error while parsing the given dateString, it outputs the result value of the provided onError expression.
        - on_null, Any : Optional. If the dateString provided to $dateFromString is null or missing, it outputs the result value of the provided onNull expression.
            
    
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
    """Returns an $dateFromString operator"""

    return DateFromString(
        date_string=date_string,
        format_=format_,
        timezone=timezone,
        on_error=on_error,
        on_null=on_null
    )