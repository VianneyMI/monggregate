"""Module defining an interface to define the fuzzy search parameters."""

from monggregate.base import BaseModel, pyd

class FuzzyOptions(BaseModel):
    """Class defining the fuzzy search parameters."""

    max_edits : int = pyd.Field(2, alias="maxEdits")
    max_expansions : int = pyd.Field(50, alias="maxExpansions")
    prefix_length : int = pyd.Field(0, alias="prefixLength")

    @property
    def statement(self) -> dict:
        
        return self.resolve(self.dict(by_alias=True))
    