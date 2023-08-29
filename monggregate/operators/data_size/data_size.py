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
class DataSizeOperatorEnum(StrEnum):
    """Enumeration of available boolean operators"""

    BINARY_SIZE    = "$binarySize" # 	Returns the size of a BinData value in bytes.
    BSON_SIZE      = "$bsonSize" # 	Returns the size of a document in bytes.


# Classes
# -----------------------------------------
class DataSizeOperator(Operator, ABC):
    """Base class for boolean operators"""

# Type aliases
# -----------------------------------------
DataSizeOperatorExpression = dict[DataSizeOperatorEnum, Any]