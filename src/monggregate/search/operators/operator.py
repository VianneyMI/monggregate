"""Operator Module"""

# Standard Library imports
#----------------------------
from abc import ABC
from typing import Literal

# Package imports
# ---------------------------
from monggregate.base import BaseModel

class SearchOperator(BaseModel, ABC):
    """MongoDB operator abstract base class"""


# Enums
# -----------------------------------------------------
OperatorLiteral = Literal[
    "autocomplete",
    "compound",
    "equals",
    "exists",
    #"facet",
    "more_like_this",
    "range",
    "regex",
    "text",
    "wildcard"
]
    