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
class ConditionalOperatorEnum(StrEnum):
    """Enumeration of available boolean operators"""

    ACCUMULATOR	= "$accumulator" # 	Defines a custom accumulator function or expression.
    FUNCTION    = "$function" # 	Defines a custom function or expression.

# Classes
# -----------------------------------------
class ConditionalOperator(Operator, ABC):
    """Base class for boolean operators"""

# Type aliases
# -----------------------------------------
ConditionalOperatorExpression = dict[ConditionalOperatorEnum, Any]