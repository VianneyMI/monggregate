"""Module defining an interface to MongoDB Atlas Search compound operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 08/05/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/compound/

# Definition
# --------------------------------------------
The compound operator combines two or more operators into a single query. 
Each element of a compound query is called a clause, and each clause consists of one or more sub-queries.

Documents in the result set are returned with a match score, 
which is calculated by summing the score that each document received 
for each individual clause which generated a match. 
The result set is ordered by score, highest to lowest.

# Syntax
# ----------------------------------------------
    >>> {
            $search: {
                "index": <index name>, // optional, defaults to "default"
                "compound": {
                <must | mustNot | should | filter>: [ { <clauses> } ],
                "score": <options>
                }
            }
        }

# Options
# ---------------------------------------------
compound uses the following terms to construct a query:

term        Description

must        Clauses that must match to for a document to be included in the results. 
            The returned score is the sum of the scores of all the subqueries in the clause.
            Maps to the AND boolean operator.

mustNot     Clauses that must not match for a document to be included in the results. 
            mustNot clauses don't contribute to a returned document's score.
            Maps to the AND NOT boolean operator.

should      Clauses that you prefer to match in documents that are included in the results. 
            Documents that contain a match for a should clause have higher scores than documents that don't contain a should clause. 
            The returned score is the sum of the scores of all the subqueries in the clause.
            Maps to the OR boolean operator.

filter      Clauses that must all match for a document to be included in the results. 
            filter clauses do not contribute to a returned document's score.

# Usage
# -------------------------------------------------------
You can use any of the clauses with any top-level operator, 
such as autocomplete, text, or span, to specify query criteria.



"""

from typing import Literal
from pydantic import Field
from monggregate.search.operators.operator import SearchOperator, Clause
from monggregate.search.operators.clause import Autocomplete

class Compound(SearchOperator):
    """
    Class defining an interface to MongoDB Atlas Search compound operator
    
    Attributes:
    ----------------------
        - must
        - must_not
        - should
        - filter
        - minimum_should_match, int : Specifies a minimum number of should clauses that must match 
                                      for a document to be included.

    # NOTE : The clauses can be nested
    """


    must : list[Clause] = []
    must_not : list[Clause] = Field([], alias="mustNot")
    should : list[Clause] = []
    filter : list[Clause] = []
    minimum_should_clause : int = 1

    def autocomplete(
            self,
            type:Literal["must", "mustNot", "should", "filter"],
            query:str|list[str], 
            path:str, 
            token_order:str="any",
            fuzzy:dict|None=None,
            score:dict|None=None,
    )->"Compound":
        
        autocomplete_statement = Autocomplete(
            query=query,
            path=path,
            token_order=token_order,
            fuzzy=fuzzy,
            score=score
        ).statement

        if type == "must":
            self.must.append(autocomplete_statement)
        elif type == "mustNot":
            self.must_not.append(autocomplete_statement)
        elif type == "filter":
            self.filter.append(autocomplete_statement)
        elif type == "should":
            self.should.append(autocomplete_statement)

        return self

