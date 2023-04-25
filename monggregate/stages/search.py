"""xxx"""

from pydantic import Field, validator
from monggregate.stages.stage import Stage

class Search(Stage):
    """"xxx"""

    index : str = "default"
    count : dict|None
    highlight : dict|None
    collector : dict|None
    operator : dict|None
    return_stored_source : bool = Field(False, alias="returnStoredSource")

    @validator("operator", pre=True, always=True)
    @classmethod
    def validate_operator(cls, value:dict, values:dict)->dict|None:
        """Ensures that either collector or operator is provided"""

        collector = values.get("collector")
        if not collector and not value:
            raise TypeError("Either collector or operator must be provided")
        
        return value
    
    @property
    def statement(self) -> dict:
    
        meta_method = self.collector or self.operator
        name, method = tuple(meta_method.items())[0]

        return {
            "$search":{
                "index":self.index,
                name:method,
                "highlight":self.highlight,
                "count":self.count,
                "retunStoredSource":self.return_stored_source
            }
        }