"""xxxx"""

from monggregate.utils import StrEnum
from monggregate.search.operators.operator import SearchOperator
#from monggregate.expressions.fields import FieldPath

class TokenOrderEnum(StrEnum):
    """xxx"""

    ANY = "any"
    SEQUENTIAL = "sequential"

class Autocomplete(SearchOperator):
    """xxx"""

    query : str
    path : str
    token_order : TokenOrderEnum = TokenOrderEnum.ANY
    fuzzy : dict
    score : dict

    @property
    def statement(self) -> dict:
        
        return {
            "autocomplete":{
                "query": self.query,
                "path": self.path,
                "tokenOrder": self.token_order,
                "fuzzy": self.fuzzy,
                "score": self.score
            }
        }