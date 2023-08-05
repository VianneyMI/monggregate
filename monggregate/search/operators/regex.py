"""
Module defining an interface to MongoDB Atlas Search regex operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 01/05/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/regex/

# Definition
# --------------------------------------------
regex interprets the query field as a regular expression. 
regex is a term-level operator, meaning that the query field isn't analyzed.

NOTE : The regular expression language available to the regex operator is a limited subset of the PCRE library.
    
       For detailed information, see the [Class RegExp](https://lucene.apache.org/core/8_0_0/core/org/apache/lucene/util/automaton/RegExp.html) documentation.

# Syntax
# --------------------------------------------
    >>> {
            $search: {
                "index": <index name>, // optional, defaults to "default"
                "regex": {
                "query": "<search-string>",
                "path": "<field-to-search>",
                "allowAnalyzedField": <boolean>,
                "score": <options>
                }
            }
        }

# Behavior
# ---------------------------------------------

regex is a term-level operator, meaning that the query field is not analyzed. 
Regular expression searches work well with the keyword analyzer, because it indexes fields one word at a time. 
To do a case-sensitive search, do not use the default analyzer, standard analyzer, because the standard analyzer lower cases all terms. 
Specify a different analyzer instead.

It is possible to use the regex operator to perform searches on an analyzed field by setting the allowAnalyzedField option to true, but you may get unexpected results.

EXAMPLE : Searching for *Star Trek* on a field indexed with the keyword analyzer finds all documents in which the field contains the string Star Trek in any context. 
          Searching for *Star Trek* on a field indexed with the standard analyzer finds nothing, because there is a space between Star and Trek, and the index contains no spaces.

# Lucene Regular Expression Behavior
---------------------------------------------

The Atlas Search regex operator uses the [Lucene regular expression engine](https://lucene.apache.org/core/8_0_0/core/org/apache/lucene/util/automaton/RegExp.html), which differs from 
[Perl Compatible Regular Expressions](https://www.pcre.org/).




"""

from monggregate.search.operators.operator import SearchOperator

class Regex(SearchOperator):
    """
    Creates a regex statement

    Description:
    ---------------------------------
    regex interprets the query field as a regular expression. 
    regex is a term-level operator, meaning that the query field isn't analyzed.
    
    Attributes:
    --------------------------------
        - query, str | list[str] : String or strings to search for.
        - path : str | list[str] : Indexed field or fields to search
                                   You can also specify a wildcard path to search.
        - allow_analyzed_field, bool : Must be set to true if the query is run against
                                       an analyzed field.
        - score, dict : Modify the score assigned to matching search term results

    """

    query : str | list[str]
    path : str | list[str]
    allow_analyzed_field: bool = False
    score : dict | None = None

    @property
    def statement(self) -> dict:
            
            return self.resolve({
                "regex":{
                    "query": self.query,
                    "path": self.path,
                    "allowAnalyzedField": self.allow_analyzed_field,
                    "score": self.score
                }
            })
    