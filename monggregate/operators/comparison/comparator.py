"""Base accumulator module"""

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
class ComparatorEnum(StrEnum):
    """Enumeration of available comparison operators"""

    CMP	= "$cmp" # Returns 0 if the two values are equivalent, 1 if thefirst value is greater than the second, and -1 if thefirst value is less than the second.
    EQ	= "$eq"	# Returns true if the values are equivalent.
    GT	= "$gt"	# Returns true if the first value is greater than thesecond.
    GTE	= "$gte" # Returns true if the first value is greater than or equalto the second.
    LT	= "$lt"	# Returns true if the first value is less than the second.
    LTE	= "$lte" # Returns true if the first value is less than or equal tothe second.
    NE	= "$ne"	# Returns true if the values are not equivalent.

# Classes
# -----------------------------------------
class Comparator(Operator, ABC):
    """Base class for accumulators"""

    left : Any
    right : Any

# Type aliases
# -----------------------------------------
ComparatorExpression = dict[ComparatorEnum, Any]