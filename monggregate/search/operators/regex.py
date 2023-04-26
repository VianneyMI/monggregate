"""xxx"""

from monggregate.search.operators.operator import SearchOperator

class Regex(SearchOperator):

    query : str
    path : str
    allow_analyzed_field: bool = False
    score : dict

    @property
    def statement(self) -> dict:
            
            return {
                "regex":{
                    "query": self.query,
                    "path": self.path,
                    "allowAnalyzedField": self.allow_analyzed_field,
                    "score": self.score
                }
            }