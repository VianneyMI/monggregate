"""Base object operator module"""

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
class ObjectOperatorEnum(StrEnum):
    """Enumeration of available object operators"""



# Classes
# -----------------------------------------
class ObjectOperator(Operator, ABC):
    """Base class for object operators"""

    MERGE_OBJECTS = "$mergeObjects" # Combines multiple documents into a single document.
    OBJECT_TO_ARRAY = "$objectToArray" # Converts a document to an array of documents representing key-value pairs.
    SET_FIELD = "$setField" # Adds, updates, or removes a specified field in a document. You can use $setField to add, update, or remove fields with names that contain periods (.) or start with dollar signs ($

# Type aliases
# -----------------------------------------
ObjectOperatorExpression = dict[ObjectOperatorEnum, Any]
