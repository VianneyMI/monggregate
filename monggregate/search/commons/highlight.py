"""
xxxx

https://www.mongodb.com/docs/atlas/atlas-search/highlighting/#syntax
"""

from typing import Literal
from pydantic import Field
from monggregate.base import BaseModel

class HighlightOptions(BaseModel):
    """xxx"""

    path : str
    max_chars_to_examine : int = Field(500000, alias="maxCharsToExamine")
    max_num_passages : int = Field(5, alias="maxNumPassages")

class HighlightText(BaseModel):
    """xxx"""

    value : str
    type : Literal["hit", "text"]

class HightlightOutput(BaseModel):
    """xxx"""

    path : str
    texts : list[HighlightText]
    score : float