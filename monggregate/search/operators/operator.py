"""Operator Module"""

# Standard Library imports
#----------------------------
from abc import ABC

# Package imports
# ---------------------------
from monggregate.base import BaseModel

class SearchOperator(BaseModel, ABC):
    """MongoDB operator abstract base class"""
    