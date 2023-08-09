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
from datetime import datetime
from typing import Literal
from monggregate.base import pyd
from monggregate.search.operators.operator import SearchOperator, Clause
from monggregate.search.operators.clause import (
    Autocomplete,
    Equals,
    Exists,
    Range,
    Regex,
    Text,
    Wilcard
    )
from monggregate.search.commons import FuzzyOptions

ClauseType = Literal["must", "mustNot", "should", "filter"]

class Compound(SearchOperator):
    """
    Class defining an interface to MongoDB Atlas Search compound operator

    Description:
    ---------------------
    The compound operator combines two or more operators into a single query. 
    Each element of a compound query is called a clause, and each clause consists of one or more sub-queries.

    Documents in the result set are returned with a match score, 
    which is calculated by summing the score that each document received for each individual clause which generated a match. 
    The result set is ordered by score, highest to lowest.
    
    Attributes:
    ----------------------
        - must, list[dict] : Clauses that must match for a document to be included in the results
        - must_not, list[dict] : Clauses that must not match for a document to be included in the results
        - should, list[dict] : Clauses that you prefer to match but that are not mandatory.
        - filter, list[dict] : Clauses that must for a document to be included but which don't affect the score.
        - minimum_should_match, int : Specifies a minimum number of should clauses that must match 
                                      for a document to be included.

    # NOTE : The clauses can be nested
    """


    must : list[Clause] = []
    must_not : list[Clause] = pyd.Field([], alias="mustNot")
    should : list[Clause] = []
    filter : list[Clause] = []
    minimum_should_clause : int = 1

    @property
    def statement(self) -> dict:


        clauses = {}
        if self.must:
            clauses["must"] = self.must
        if self.must_not:
            clauses["mustNot"] = self.must_not
        if self.should:
            clauses["should"] = self.should
        if self.filter:
            clauses["filter"] = self.filter

        return self.resolve({
                "compound":clauses
            })

    def _register_clause(self, type:ClauseType, statement:dict)->None:
        """
        Adds a clause to the current compound instance.

        Attributes:
        -----------------------
            - type:Literal["must", "mustNot", "should", "filter"] : The type of clause to add
            - statement:dict : The operator statement of the clause to add
        
        
        """

        if type == "must":
            self.must.append(statement)
        elif type == "mustNot":
            self.must_not.append(statement)
        elif type == "filter":
            self.filter.append(statement)
        elif type == "should":
            self.should.append(statement)


    def autocomplete(
            self,
            type:ClauseType,
            *,
            query:str|list[str], 
            path:str, 
            token_order:str="any",
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
    )->"Compound":
        """Adds an autocomplete clause to the current compound instance."""
        
        autocomplete_statement = Autocomplete(
            query=query,
            path=path,
            token_order=token_order,
            fuzzy=fuzzy,
            score=score
        ).statement

        self._register_clause(type, autocomplete_statement)
    
        return self
    
    def equals(
            self,
            type,
            path:str,
            value:str|int|float|bool|datetime,
            score:dict|None=None
    )->"Compound":
        """Adds an equals clause to the current compound instance."""

        equals_statement = Equals(
            path=path,
            value=value,
            score=score
        ).statement

        self._register_clause(type, equals_statement)

        return self

    def exists(self, type:ClauseType, path:str)->"Compound":
        """Adds an exists clause to the current compound instance."""

        exists_statement = Exists(path=path).statement
        self._register_clause(type, exists_statement)

        return self

    def range(
            self,
            type:ClauseType,
            *,
            path:str|list[str],
            gt:int|float|datetime|None=None,
            lt:int|float|datetime|None=None,
            gte:int|float|datetime|None=None,
            lte:int|float|datetime|None=None,
            score:dict|None=None
    )->"Compound":
        """Adds a range clause to the current compound instance."""

        range_statement = Range(
            path=path,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            score=score
        ).statement

        self._register_clause(type, range_statement)

        return self

    def regex(
            self,
            type:ClauseType,
            *,
            query:str|list[str],
            path:str|list[str],
            allow_analyzed_field:bool=False,
            score:dict|None=None
    )->"Compound":
        """Adds a regex clause to the current compound instance."""

        regex_statement = Regex(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        ).statement


        self._register_clause(type, regex_statement)

        return self

    def text(
            self,
            type:ClauseType,
            *,
            query:str|list[str],
            path:str|list[str],
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            synonyms:str|None=None
    )->"Compound":
        """Adds a text clause to the current compound instance."""

        text_statement = Text(
            query=query,
            path=path,
            score=score,
            fuzzy=fuzzy,
            synonyms=synonyms
        ).statement

        self._register_clause(type, text_statement)

        return self

    def wildcard(
            self,
            type:ClauseType,
            *,
            query:str|list[str],
            path:str|list[str],
            allow_analyzed_field:bool=False,
            score:dict|None=None,
    )->"Compound":
        """Adds a wildcard clause to the current compound instance."""

        wildcard_statement = Wilcard(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        ).statement

        self._register_clause(type, wildcard_statement)

        return self
    