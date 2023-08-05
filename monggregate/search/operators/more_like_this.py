"""
Module defining an interface to MongoDB Atlas Search moreLikeThis operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 30/04/2023
Source : hhttps://www.mongodb.com/docs/atlas/atlas-search/morelikethis/

# Definition
# --------------------------------------------

The moreLikeThis operator returns documents similar to input documents. 
The moreLikeThis operator allows you to build features for your applications that display 
similar or alternative results based on one or more given documents.

# Behavior
# --------------------------------------------

When you run a moreLikeThis query, Atlas Search performs these actions:

    * Extracts a limited number of most representative terms based on the input documents that you specify in the operator's like option.

    * Creates a disjunction (OR) query to find similar documents based on the most representative terms and returns the results.

The moreLikeThis operator performs a search for similar documents using the analyzer that you specify in the index configuration. 
If you omit the analyzer in the index definition, the moreLikeThis operator uses the default standard analyzer. If you specify multiple analyzers, the moreLikeThis operator runs the input text through each analyzer, searches, and returns results for all analyzers.

To view the disjunction (OR) that Atlas Search constructs to find similar documents, use explain with your moreLikeThis operator query.

# Usage
# --------------------------------------------

Before you can run the moreLikeThis operator query, we recommend that you retrieve one or more input documents. To retrieve input documents, you can do one of the following:

    * Run a query, such as find(), or another MQL query to find BSON documents.

    * Run any aggregation pipeline that returns BSON documents.

    * Use any other source of documents in your application.

Once you identify the input documents, you can pass them to the moreLikeThis operator.

When you run a moreLikeThis operator query, Atlas Search returns the original input document in the query results. 
To omit the input document from the query results, 
use the moreLikeThis operator in a compound operator query and exclude the input document by its _id using the equals operator in the mustNot clause.

# Syntax
# ----------------------------------------------

moreLikeThis has the following syntax:

    >>> {
            "$search": {
                "index": index name, // optional, defaults to "default"
                "moreLikeThis": {
                "like": [
                    {
                    <"field-name">: <"field-value">,
                    ...
                    },
                    ...
                ],
                ...
                }
            }
        }

# Options
# ---------------------------------------------
moreLikeThis uses the following option to constuct a query:

Field   Type                            Description                                             Necessity
like    one BSON document               One or more BSON documents that Atlas Search            Yes
        or an array of documents        uses to extract representative terms to query for.
        


# Limitations
# ---------------------------------------------
You can't use the moreLikeThis operator to query non-string values. 
To search for non-string values, you can combine a moreLikeThis query with a near, range, or any other operator in a compound operator query.

You can't use the moreLikeThis operator inside the embeddedDocument operator to query documents in an array.

"""

from monggregate.base import pyd
from monggregate.search.operators.operator import SearchOperator


class MoreLikeThis(SearchOperator):
    """
    Creates a moreLikeThis operator statement in an Atlas Search query.

    Description:
    ----------------------------------------------
    The moreLikeThis operator returns documents similar to input documents.

    Attributes:
    ----------------------------------------------
    like, dict | list[dict] : One or more BSON documents that Atlas Search uses to extract representative terms to query for.
    
    """

    like : dict | list[dict]

    @pyd.validator("like", pre=True, always=True)
    def validate_like(cls, v):
        if isinstance(v, list):
            if len(v)==0:
                raise ValueError("The 'like' field must be a non-empty list of BSON documents.")

        return v
    
    @property
    def statement(self) -> dict:
        
        return self.resolve({
            "moreLikeThis" : {
                "like" : self.like
            }
        })
    