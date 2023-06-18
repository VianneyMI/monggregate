"""
Module defining an interface to MongoDB Atlas Search autocomplete operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 26/04/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/autocomplete/

# Definition
# --------------------------------------------

The autocomplete operator performs a search for a word or phrase that contains 
a sequence of characters from an incomplete input string. 
You can use the autocomplete operator with search-as-you-type applications 
to predict words with increasing accuracy as characters are entered in your application's search field. autocomplete returns results that contain predicted words based on the tokenization strategy specified in the index definition for autocompletion. The fields that you intend to query with the autocomplete operator must be indexed with the How to Index Fields for Autocompletion data type in the collection's index definition.

NOTE : Atlas Search might return inaccurate results for queries with more than three words in a single string.


# Syntax
# ----------------------------------------------

autocomplete has the following syntax:

    >>> {
            $search: {
                "index": "<index name>", // optional, defaults to "default"
                "autocomplete": {
                "query": "<search-string>",
                "path": "<field-to-search>",
                "tokenOrder": "any|sequential",
                "fuzzy": <options>,
                "score": <options>
                }
            }
        }

# Options
# ---------------------------------------------


Field       Type            Description                             Necessity       Default

query       string          String or strings to search for.        Yes
            (or array of    If there are multiple terms in
            strings)        a string. Atlas Search also looks
                            for a match for each term in the
                            string separately.

path        string          Indexed autocomplete type of field      Yes
                            to search.
                            NOTE : The autocomplete operator
                            does not support multi in the field
                            path.

fuzzy       object          Enable fuzzy search. Find strings       no 
                            which are similar to the search 
                            term or terms.

                            
fuzzy
.maxEdits   integer         Maximum number of single-character      no              2
                            edits required to match the specified
                            specified search term. 
                            Value can be 1 or 2.

fuzzy       integer         Number of characters at the begining    no              0
.prefix                     of each term in the result that must
Length                      exactly match.  


fuzzy       integer         Maximum number of variations to         no              50
.max                        generate and search for. This limit
Expansions                  applies on a per-token basis

score       object          score assigned to matching search       no
                            term results. 
                            Use one of the following
                            options to modify the score:

                            boost    |Multiply the results score 
                                     |by the given number.

                            constant |Replace the result score 
                                     |with the given number.

                            NOTE: autocomplete offers less 
                            fidelity in score in exchange 
                            or faster query execution

tokenOder   str             Order in which to search for tokens.    no              any                  
                            Value can be one of the following:

                            any       |Indicates tokens in the
                                      |query can appear in any
                                      |order in the documents.
                                      |Results contain documents
                                      |where the tokens appear
                                      |sequentially and 
                                      |non-sequentially.
                                      |However, results where the 
                                      |tokens appear sequantially
                                      |score higher
        

                            sequen-   |Indicates tokens in the query
                            tial      |must appear adjacent to each
                                      |other or in the order specified
                                      |in the query in the docuents.
                                      |Results contain only documents
                                      |where the tokens appear
                                      |sequentially.

# Limitations
# -----------------------------

The autocomplete operator query results that are exact matches receive a lower score than results that aren't exact matches. 
Atlas Search can't determine if a query string is an exact match for an indexed text if you specify just the autocomplete-indexed token substrings. 
To score exact matches higher, try the following workaround:

NOTE : The following workaround doesn't guarantee higher scores for exact matches in all cases.

    1. Index the field as both [How to Index Fields for Autocompletion](https://www.mongodb.com/docs/atlas/atlas-search/field-types/autocomplete-type/#std-label-bson-data-types-autocomplete) 
       and [How to Index String Fields types](https://www.mongodb.com/docs/atlas/atlas-search/field-types/string-type/#std-label-bson-data-types-string).

    2. Query using the compound operator.

For a demonstration of this workaround, [see Compound Example](https://www.mongodb.com/docs/atlas/atlas-search/autocomplete/#std-label-autocomplete-compound).

"""

from monggregate.utils import StrEnum
from monggregate.search.operators.operator import SearchOperator
from monggregate.search.commons import FuzzyOptions
#from monggregate.expressions.fields import FieldPath

class TokenOrderEnum(StrEnum):
    """Enumeration of possible values for tokenOrder parameter"""

    ANY = "any"
    SEQUENTIAL = "sequential"

class Autocomplete(SearchOperator):
    """
    Creates an autocomplete operation statement in an Atlas Search query.

    Description:
    -------------------------------
    The autocomplete operator performs a search for a word or phrase that contains a sequence of characters from an incomplete input string. 
    You can use the autocomplete operator with search-as-you-type applications to predict words with increasing accuracy as characters are entered in your application's search field. 
    autocomplete returns results that contain predicted words based on the tokenization strategy specified in the index definition for autocompletion. 
    The fields that you intend to query with the autocomplete operator must be indexed with the How to Index Fields for Autocompletion data type in the collection's index definition.

    Attributes:
    -------------------------------
        - query, str|list[str] : String or strings to search for. If there are multiple
                                 terms in a string, Atlas Search also looks for a match
                                 for each term in the string separately.
        - path, str : Indexed autocomplete type of field to search.
        - fuzzy, FuzzyOptions : Enable fuzzy search. Find strings which are similar to the search 
                       term or terms.
        - score, dict : score assigned to matching search term results
        - token_order, "any"|"sequential" : Order in which to search for tokens.
    
    """

    query : str|list[str]
    path : str
    token_order : TokenOrderEnum = TokenOrderEnum.ANY
    fuzzy : FuzzyOptions|None
    score : dict|None

    @property
    def statement(self) -> dict:
        
        return self.resolve({
            "autocomplete":{
                "query": self.query,
                "path": self.path,
                "tokenOrder": str(self.token_order),
                "fuzzy": self.fuzzy,
                "score": self.score
            }
        })
    