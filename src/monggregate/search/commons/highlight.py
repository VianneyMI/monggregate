"""
Module defining an interface to define the highlighting parameters.

https://www.mongodb.com/docs/atlas/atlas-search/highlighting/#syntax
"""

from typing import Literal

from monggregate.base import BaseModel, pyd

class HighlightOptions(BaseModel):
    """Class defining the highlighting parameters."""

    path : str
    max_chars_to_examine : int = pyd.Field(500000, alias="maxCharsToExamine")
    max_num_passages : int = pyd.Field(5, alias="maxNumPassages")

class HighlightText(BaseModel):
    """Highlighted text."""

    value : str
    type : Literal["hit", "text"]

class HightlightOutput(BaseModel):
    """Class defining the highlights appear in a search query results."""

    path : str
    texts : list[HighlightText]
    score : float
