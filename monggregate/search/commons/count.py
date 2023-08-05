"""
Module defining an interface to define the count parameters in search queries.
https://www.mongodb.com/docs/atlas/atlas-search/counting/#std-label-count-ref

"""

from typing import Literal

from monggregate.base import BaseModel, pyd

class CountOptions(BaseModel):
    """Class defining the count parameters."""

    type : Literal["lowerBound", "total"] = "lowerBound"
    threshold : int = 1000

    @property
    def statement(self) -> dict:
        
        return self.resolve(self.dict(by_alias=True))
    
class CountResults(BaseModel):
    """Class defining the count results."""

    lower_bound : int|None = pyd.Field(None, alias="lowerBound")
    total : int|None