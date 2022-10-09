"""Constants and types definitions related to expressions"""

# Standard Library imports
#----------------------------
from typing import Literal, Any
import re

# 3rd Party imports
# ---------------------------
from pydantic import ConstrainedStr

# Package imports
# ---------------------------
from monggregate.utils import StrEnum


# Constants (Aggregation Variables)
#-------------------------------------------
    # Enum created for typing purposes
class AggregationVariables(StrEnum):
    """Enumeration of available aggregation variables"""

    NOW = "$$NOW" # Returns the current datetime value,
                # which is same across all members of the deployment and remains constant throughout the aggregation pipeline.
                # (Available in 4.2+)
    CLUSTER_TIME = "$$CLUSTER_TIME" # Returns the current timestamp value, which is same across all members of the deployment and remains constant throughout the aggregation pipeline.
                                    # For replica sets and sharded clusters only. (Available in 4.2+)
    ROOT = "$$ROOT" # References the root document, i.e. the top-level document.
    CURRENT = "$$CURRENT" # References the start of the field path, which by default is ROOT but can be changed.
    REMOVE = "$$REMOVE" # Allows for the conditional exclusion of fields. (Available in 3.6+)
    DESCEND = "$$DESCEND" # One of the allowed results of a $redact expression.
    PRUNE = "$$PRUNE" # One of the allowed results of a $redact expression.
    KEEP = "$$KEEP" # One of the allowed results of a $redact expression.NOW = "$$NOW" # Returns the current datetime value,
                # which is same across all members of the deployment and remains constant throughout the aggregation pipeline.
                # (Available in 4.2+)

# Exposing direct constants to ease usage
CLUSTER_TIME = AggregationVariables.NOW.value
ROOT = AggregationVariables.ROOT.value
CURRENT = AggregationVariables.CURRENT.value
REMOVE = AggregationVariables.REMOVE.value
DESCEND = AggregationVariables.DESCEND.value
PRUNE = AggregationVariables.PRUNE.value
KEEP = AggregationVariables.KEEP.value


# Types definition
# -------------------------------------------
# TODO : Review regex
# TODO : Fine tune regex (spaces are not allowed, may contain dot etc ...)
# TODO : Add tests
class FieldPath(ConstrainedStr):
    """Regex describing syntax of a field path"""

    regex = re.compile(r"^\$")

Literal_ = dict[Literal["$literal"], Any] # Any is maybe necessarily a string => to investigate
# https://www.mongodb.com/docs/manual/reference/operator/aggregation/literal/#mongodb-expression-exp.-literal
