"""Base boolean operator module"""

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
class BooleanOperatorEnum(StrEnum):
    """Enumeration of available boolean operators"""

    AND	= "$and" #  Returns true only when all its expressions evaluate to true . Accepts any number of argument expressions.
    NOT	= "$not" # 	Returns the boolean value that is the opposite of itsargument expression. Accepts a single argument expression.
    OR	= "$or"	# Returns true when any of its expressions evaluates to true . Accepts any number of argument expressions.


# Classes
# -----------------------------------------
class BooleanOperator(Operator, ABC):
    """Base class for boolean operators"""

# Type aliases
# -----------------------------------------
BooleanOperatorExpression = dict[BooleanOperatorEnum, Any]
