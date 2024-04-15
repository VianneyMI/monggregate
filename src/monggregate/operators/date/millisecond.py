"""
Module defining an interface to $millisecond operator

Online MongoDB documentation
----------------------------
Returns the millisecond portion of a date as an integer between 0 and 999.

The $millisecond expression has the following operator expression syntax:

    >>> { $millisecond: <dateExpression> }

The argument can be:

* An expression that resolves to a Date, a Timestamp, or an ObjectID.
* A document with this format:

    >>> { date: <dateExpression>, timezone: <tzExpression> }

        Field       Description
    *   date        The date to which the operator is applied. 
                    <dateExpression> must be a valid expression 
                    that resolves to a Date, a Timestamp, or an ObjectID.
    *   timezone    Optional. The timezone of the operation result. 
                    <tzExpression> must be a valid expression that 
                    resolves to a string formatted as either an Olson 
                    Timezone Identifier or a UTC Offset. If no timezone is 
                    provided, the result is displayed in UTC.

                        Format                      Examples
                    *   Olson Timezone Identifier   "America/New_York"
                                                    "Europe/London"
                                                    "GMT"

                    *   UTC Offset                  +/-[hh]:[mm], e.g. "+04:45"
                                                    +/-[hh][mm], e.g. "-0530"
                                                    +/-[hh], e.g. "+03"


Behavior
--------

Example                                                         Result

    >>> { $millisecond: new Date("2016-01-01") }                0

    >>> { $millisecond: { date: new Date("Jan 7, 2003") } }     0

    >>> { $millisecond: {                                       0
    date: new Date("August 14, 2011"),
    timezone: "America/Chicago"
        } }

    >>> { $millisecond: ISODate("1998-11-07T00:00:00Z") }       0

    >>> { $millisecond: {                                       0
    date: ISODate("1998-11-07T00:00:00Z"),
    timezone: "-0400"
        } }

    >>> { $millisecond: "March 28, 1976" }                      error

    >>> { $millisecond: Date("2016-01-01") }                    error
    
    >>> { $millisecond: "2009-04-09" }                          error

NOTE

**$millisecond cannot take a string as an argument.**

Example
-------
Consider a sales collection with the following document:

    >>> {
    "_id" : 1,
    "item" : "abc",
    "price" : 10,
    "quantity" : 2,
    "date" : ISODate("2014-01-01T08:15:39.736Z")
    }

The following aggregation uses the $millisecond and other date operators to break down the date field:

    >>> db.sales.aggregate(
    [
        {
        $project:
            {
            year: { $year: "$date" },
            month: { $month: "$date" },
            day: { $dayOfMonth: "$date" },
            hour: { $hour: "$date" },
            minutes: { $minute: "$date" },
            seconds: { $second: "$date" },
            milliseconds: { $millisecond: "$date" },
            dayOfYear: { $dayOfYear: "$date" },
            dayOfWeek: { $dayOfWeek: "$date" },
            week: { $week: "$date" }
            }
        }
    ]
    )

The operation returns the following result:

    >>> {
    "_id" : 1,
    "year" : 2014,
    "month" : 1,
    "day" : 1,
    "hour" : 8,
    "minutes" : 15,
    "seconds" : 39,
    "milliseconds" : 736,
    "dayOfYear" : 1,
    "dayOfWeek" : 4,
    "week" : 0
    }
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
    
    Online MongoDB documentation
    ----------------------------
    Returns the millisecond portion of a date as an integer between 0 and 999.

    The $millisecond expression has the following operator expression syntax:

        >>> { $millisecond: <dateExpression> }

    The argument can be:

    * An expression that resolves to a Date, a Timestamp, or an ObjectID.
    * A document with this format:

        >>> { date: <dateExpression>, timezone: <tzExpression> }

            Field       Description
        *   date        The date to which the operator is applied. 
                        <dateExpression> must be a valid expression 
                        that resolves to a Date, a Timestamp, or an ObjectID.
        *   timezone    Optional. The timezone of the operation result. 
                        <tzExpression> must be a valid expression that 
                        resolves to a string formatted as either an Olson 
                        Timezone Identifier or a UTC Offset. If no timezone is 
                        provided, the result is displayed in UTC.

                            Format                      Examples
                        *   Olson Timezone Identifier   "America/New_York"
                                                        "Europe/London"
                                                        "GMT"

                        *   UTC Offset                  +/-[hh]:[mm], e.g. "+04:45"
                                                        +/-[hh][mm], e.g. "-0530"
                                                        +/-[hh], e.g. "+03"
                                                        
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