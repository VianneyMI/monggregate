"""xxxx"""

from datetime import datetime
from monggregate.search.operators.operator import SearchOperator

class Equals(SearchOperator):
    """xxx"""

    path : str
    value : str | int | float | bool | datetime
    score : dict

    @property
    def statement(self) -> dict:
            
            return {
                "equals":{
                    "path": self.path,
                    "value": self.value,
                    "score": self.score
                }
            }