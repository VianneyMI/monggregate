"""
Module defining an interface to MongoDB Atlas Search wildcard operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 01/05/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/text/

# Definition
# -------------------------------------------
The wildcard operator enables queries which use special characters in the search string that can match any character.

Character   Description

?           Matches any single character.
*           Matches 0 or more characters.
\           Escape character.

wildcard is a term-level operator, meaning that the query field is not analyzed. 
Term-level operators work well with the Keyword Analyzer, because the query field is treated as a single term, with special characters included. 
For an example of querying against an analyzed query field vs. a non-analyzed query field, see the analyzed field example.

# Syntax
# -------------------------------------------
wildcard has the following syntax:

    >>> {
            $search: {
                "index": <index name>, // optional, defaults to "default"
                "wildcard": {
                "query": "<search-string>",
                "path": "<field-to-search>",
                "allowAnalyzedField": <boolean>,
                "score": <options>
                }
            }
        }

# Behavior
# ------------------------------------------
wildcard is a term-level operator, meaning that the query field is not analyzed. 
It is possible to use the wildcard operator to perform searches on a field analyzed during indexing by setting the allowAnalyzedpyd.Field option to true, 
but results will reflect that the query text is not analyzed.

EXAMPLE : Suppose that a field foo bar baz is indexed with the standard analyzer. Atlas Search analyzes and indexes the field as foo, bar and baz. 
          Searching for foo bar* on this field finds nothing, because the wildcard operator treats foo bar* as a single search term with a wildcard at the end. 
          In other words, Atlas Search searches the field for any term that begins with foo bar but finds nothing, because no term exists.

EXAMPLE : Searching for *Star Trek* on a field indexed with the keyword analyzer finds all documents in which the field contains the string Star Trek in any context. 
          Searching for *Star Trek* on a field indexed with the standard analyzer finds nothing, because there is a space between Star and Trek, and the index contains no spaces.

# Escape Character Behavior
# ---------------------------------------

When using the escape character in mongosh or with a driver, you must use a double backslash before the character to be escaped.

EXAMPLE : To create a wildcard expression which searches for any string containing a literal asterisk in an aggregation pipeline, use the following expression:
          >>>  "*\\**"

          The first and last asterisks act as wildcards which match any characters, and the \\* matches a literal asterisk.

          NOTE : Use the following expression to escape a literal backslash:

          >>> "*\\\*"

"""

from monggregate.base import pyd
from monggregate.search.operators.operator import SearchOperator

class Wilcard(SearchOperator):
    """
    Creates a wilcard operation statement in an Atlas Search query.

    Description:
    ------------------------------------------- 
    The wildcard operator enables queries which use special characters in the search string that can match any character.

    Attributes
    -------------------------------------------
        - query, str | list[str] : String or strings to search for
        - path : str | list[str] : Indexed field or fields to search.
        - allow_analyzed_field, bool : Must be set to true if the query is run against
                                       an analyzed field. Defaults to false.
        - score, dict : Scoring options
    
    """

    query : str | list[str]
    path : str | list[str]
    allow_analyzed_field : bool = pyd.Field(False, alias="allowAnalyzedField")
    score : dict | None = None

    @property
    def statement(self) -> dict:
        
        return self.resolve({
            "wildcard":self.dict(exclude_none=True, by_alias=True)
        })