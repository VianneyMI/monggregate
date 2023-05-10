"""Collector Module"""

# Standard Library imports
#----------------------------
from abc import ABC

# Package imports
# ---------------------------
from monggregate.base import BaseModel

class SearchCollector(BaseModel, ABC):
    """MongoDB operator abstract base class"""