"""xxx"""

from monggregate.search.operators.operator import SearchOperator

class Wilcard(SearchOperator):

    query : str | list[str]
    path : str
    allow_analyzed_field : bool = False
    score : dict
    