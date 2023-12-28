"""
Module defining an interface to define the count parameters in search queries.
https://www.mongodb.com/docs/atlas/atlas-search/counting/#std-label-count-ref

"""

from typing import Literal

from monggregate.base import BaseModel, pyd

class CountOptions(BaseModel):
    """Class representing the count options in a $search query.
    
    `count` option adds a field to the metadata results document that displays a count of the search results for the query.

    Attributes:
    --------------------------------
    - type : str
        Type of count of the documents in the result set. Value can be one of the following:
            - lowerBound : for a lower bound count of the number of documents that match the query. 
                           You can set the threshold for the lower bound number.
            - total : for an exact count of the number of documents that match the query. 
                      If the result set is large, Atlas Search might take longer than for lowerBound to return the count.
        If omitted, the default value is lowerBound.
    - threshold : int
        Number of documents to include in the exact count if type is lowerBound. 
        If omitted, defaults to 1000, which indicates that any number up to 1000 is an exact count 
        and any number above 1000 is a rough count of the number of documents in the result.
    
    """

    type : Literal["lower_bound", "lowerBound", "total"] = "lowerBound"
    threshold : int = 1000

    @pyd.validator("type", pre=True, always=True)
    def validate_type(cls, value:str)->str:
        """Pre-validates the type field."""

        if value == "lower_bound":
            return "lowerBound"
        return value

    @property
    def statement(self) -> dict:
        
        return self.resolve(self.dict(by_alias=True))
    
class CountResults(BaseModel):
    """Class defining the count results."""

    lower_bound : int|None
    total : int|None

    @property
    def statement(self) -> dict:
        
        return self.resolve(self.dict(by_alias=True))