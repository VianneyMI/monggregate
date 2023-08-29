# Standard Library Imports
# -----------------------------------------
from abc import ABC
from typing import Any

# Local imports
# -----------------------------------------
from monggregate.operators import Operator
from monggregate.utils import StrEnum

# Enums
# -----------------------------------------
class DateOperatorEnum(StrEnum):
    """Enumeration of available boolean operators"""

    DATE_ADD    = "$dateAdd" # 	Adds the specified number of units to a date expression.
    DATE_DIFF   = "$dateDiff" # 	Returns the difference between two date expressions in the specified time unit.
    DATE_FROM_PARTS = "$dateFromParts" # 	Returns a date given the date’s constituent properties.
    DATE_FROM_STRING = "$dateFromString" # 	Converts a date/time string to a date object.
    DATE_SUBTRACT = "$dateSubtract" # 	Subtracts the specified number of units from a date expression.
    DATE_TO_PARTS = "$dateToParts" # 	Returns a document containing the constituent parts of a date.
    DATE_TO_STRING = "$dateToString" # 	Converts a date object to a string according to a user-specified format.
    DATE_TRUNC = "$dateTrunc" # 	Returns a date with the specified part(s) reset to a set value.
    DAY_OF_MONTH = "$dayOfMonth" # 	Returns the day of the month for a date as a number between 1 and 31.
    DAY_OF_WEEK = "$dayOfWeek" # 	Returns the day of the week for a date as a number between 1 (Sunday) and 7 (Saturday).
    DAY_OF_YEAR = "$dayOfYear" # 	Returns the day of the year for a date as a number between 1 and 366 (leap year).
    HOUR = "$hour" # 	Returns the hour portion of a date as a number between 0 and 23.
    ISO_DAY_OF_WEEK = "$isoDayOfWeek" # 	Returns the weekday number in ISO 8601 format, ranging from 1 (for Monday) to 7 (for Sunday).
    ISO_WEEK = "$isoWeek" # 	Returns the week number in ISO 8601 format, ranging from 1 to 53. Week numbers start at 1 with the week (Monday through Sunday) that contains the year’s first Thursday.
    ISO_WEEK_YEAR = "$isoWeekYear" # 	Returns the year number in ISO 8601 format. The year starts with the Monday of week 1 (ISO 8601) and ends with the Sunday of the last week (ISO 8601).
    MILLISECOND = "$millisecond" # 	Returns the millisecond portion of a date as an integer between 0 and 999.
    MINUTE = "$minute" # 	Returns the minute portion of a date as a number between 0 and 59.
    MONTH = "$month" # 	Returns the month of a date as a number between 1 and 12.
    SECOND = "$second" # 	Returns the second portion of a date as a number between 0 and 59, but can be 60 to account for leap seconds.
    TO_DATE = "$toDate" # 	Converts a value of any type to a date.
    WEEK = "$week" # 	Returns the week number for a date as a number between 0 (the partial week that precedes the first Sunday of the year) and 53 (leap year).
    YEAR = "$year" # 	Returns the year portion of a date as a number (e.g. 2014).





# Classes
# -----------------------------------------
class DateOperator(Operator, ABC):
    """Base class for boolean operators"""

# Type aliases
# -----------------------------------------
DateOperatorExpression = dict[DateOperatorEnum, Any]