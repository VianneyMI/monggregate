"""xxx"""

from monggregate.search.operators.operator import SearchOperator

class MoreLikeThis(SearchOperator):

    like : dict | list[dict]