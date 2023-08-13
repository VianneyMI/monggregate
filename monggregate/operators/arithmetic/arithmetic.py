"""Base arithmetic operator module"""

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
class ArithmeticOperatorEnum(StrEnum):
    """Enumeration of available arithmetic operators"""

    ABS = "$abs" # Returns the absolute value of a number. Accepts a single argument expression.
    ADD = "$add" # Adds numbers together or adds numbers and a date. Accepts any number of argument expressions, but at most, one expression can resolve to a date.
    CEIL = "$ceil" # Returns the smallest integer greater than or equal to the specified number. Accepts a single argument expression.
    DIVIDE = "$divide" # Divides one number by another and returns the result. Accepts two argument expressions.
    EXP = "$exp" # Raises Euler’s number to the specified exponent and returns the result. Accepts a single argument expression.
    FLOOR = "$floor" # Returns the largest integer less than or equal to the specified number. Accepts a single argument expression.
    LN = "$ln" # Calculates the natural logarithm ln (i.e loge) of a number and returns the result as a double. Accepts a single argument expression.
    LOG = "$log" # Calculates the log of a number in the specified base and returns the result as a double. Accepts two argument expressions.
    LOG10 = "$log10" # Calculates the log base 10 of a number and returns the result as a double. Accepts a single argument expression.
    MOD = "$mod" # Performs a modulo operation on the first argument and returns the remainder. Accepts two argument expressions.
    MULTIPLY = "$multiply" # Multiplies numbers together and returns the result. Accepts any number of argument expressions.
    POW = "$pow" # Raises a number to the specified exponent and returns the result. Accepts two argument expressions.
    ROUND = "$round" # Rounds a number to to a whole integer or to a specified decimal place. Accepts two argument expressions.
    SQRT = "$sqrt" # Calculates the square root of a positive number and returns the result as a double. Accepts a single argument expression.
    SUBTRACT = "$subtract" # Subtracts two numbers to return the difference, or adds two numbers to return the sum. Accepts two argument expressions. If both arguments are dates, $subtract returns the difference in milliseconds.
    TRUNC = "$trunc" # Truncates a number to a whole integer or to a specified decimal place. Accepts a single argument expression.

# Classes
# -----------------------------------------
class ArithmeticOperator(Operator, ABC):
    """Base class for arithmetic operators"""

# Type aliases
# -----------------------------------------
ArithmeticOperatorExpression = dict[ArithmeticOperatorEnum, Any]