"""xxx"""

from datetime import datetime
from monggregate.search.operators.operator import SearchOperator

class Range(SearchOperator):

    path : str
    gt : int | float | datetime | None
    lt : int | float | datetime | None
    gte : int | float | datetime | None
    lte : int | float | datetime | None
    score : dict

    @validator("gte", pre=True, always=True)
    def at_least_one_lower(cls, value, values):
        if value is None and values.get("gt") is None:
            raise ValueError("at least one of gte or gt must be specified")
        return value
    
    @validator("lte", pre=True, always=True)
    def at_least_one_upper(cls, value, values):
        if value is None and values.get("lt") is None:
            raise ValueError("at least one of lte or lt must be specified")
        return value


    @property
    def statement(self) -> dict:
            
            params = {
                "path": self.path,
                "score": self.score
            }
            
            if self.gt is not None:
                params["gt"] = self.gt
            else:
                params["gte"] = self.gte

            if self.lt is not None:
                params["lt"] = self.lt
            else:
                params["lte"] = self.lte

            return {"range":params}