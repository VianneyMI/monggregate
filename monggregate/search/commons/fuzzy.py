"""Module defining an interface to define the fuzzy search parameters."""

from pydantic import Field
from monggregate.base import BaseModel

class FuzzyOptions(BaseModel):
    """Class defining the fuzzy search parameters."""

    max_edits : int = Field(2, alias="maxEdits")
    max_expansions : int = Field(50, alias="maxExpansions")
    prefix_length : int = Field(0, alias="prefixLength")

    @property
    def statement(self) -> dict:
        
        return self.dict(by_alias=True)
    