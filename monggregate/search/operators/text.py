"""xxx"""

from monggregate.search.operators.operator import SearchOperator

class Text(SearchOperator):

    query : str|list[str]
    path : str
    fuzzy : dict
    score : dict
    synonyms : dict