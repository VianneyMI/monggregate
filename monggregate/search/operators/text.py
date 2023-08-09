"""
Module defining an interface to MongoDB Atlas Search text operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 01/05/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/text/

# Definition
# -------------------------------------------
The text operator performs a full-text search using the analyzer that you specify in the index configuration. 
If you omit an analyzer, the text operator uses the default standard analyzer.

# Syntax
#--------------------------------------------
text has the following syntax:

    >>> {
            $search: {
                "index": <index name>, // optional, defaults to "default"
                "text": {
                "query": "<search-string>",
                "path": "<field-to-search>",
                "fuzzy": <options>,
                "score": <options>,
                "synonyms": "<synonyms-mapping-name>"
                }
            }
        }


"""

from monggregate.search.operators.operator import SearchOperator
from monggregate.search.commons.fuzzy import FuzzyOptions

class Text(SearchOperator):
    """
    Creates a text operation statement in an Atlas Search query.

    Description:
    ----------------------------------------
    The text operator performs a full-text search using the analyzer that you specify in the index configuration. 
    If you omit an analyzer, the text operator uses the default standard analyzer.

    Attributes:
    -----------------------------------------
        - query, str | list[str] : The string or strings to search for.
                                   If there are multiple terms in a string,
                                   Atlas Search also looks for a match for
                                   each term in the string separately
        - path, str | list[str] : Indexed field or fields to search in. 
                                  You can also specify a wildcard path
                                  to search.
        - fuzzy, FuzzyOptions : Enable fuzzy search. Find strings which are 
                        similar to the search term or terms. You can't use fuzzy with synonyms.

        - synonyms, str : Name of the synonym mapping definition in the index definition. 
                          Value can't be an empty string. You can't use fuzzy with synonyms.

                          text queries that use synonyms look for a conjunction (AND) of query
                          tokens. text queries that don't use synonyms search for a disjunction (OR)
                          of query tokens. To run text queries that use syninyms and search for
                          a disjunction (OR) of query tokens also, use the coumpound operator.

    """

    query : str|list[str]
    path : str | list[str]
    fuzzy : FuzzyOptions | None = None
    score : dict | None = None
    synonyms : str | None = None

    @property
    def statement(self) -> dict:
        
        return self.resolve({
            "text" : self.dict(exclude_none=True, by_alias=True)
        })
            