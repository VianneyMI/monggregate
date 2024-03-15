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
from typing import Any, Literal, Callable

from typing_extensions import Self

from monggregate.base import pyd
from monggregate.search.operators.operator import SearchOperator, OperatorLiteral
from monggregate.search.operators.clause import (
    Clause,
    Autocomplete,
    Equals,
    Exists,
    MoreLikeThis,
    Range,
    Regex,
    Text,
    Wildcard
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


    must : list["Clause|Compound"] = []
    must_not : list["Clause|Compound"] = []
    should : list["Clause|Compound"] = []
    filter : list["Clause|Compound"] = []
    minimum_should_match : int = 0

    @property
    def statement(self) -> dict:

        clauses = {}
        if self.must:
            clauses["must"] = self.must
        if self.must_not:
            clauses["mustNot"] = self.must_not
        if self.should:
            clauses["should"] = self.should
            clauses["minimumShouldMatch"] = self.minimum_should_match
        if self.filter:
            clauses["filter"] = self.filter

        return self.resolve({
                "compound":clauses
            })

    def _register_clause(self, type:ClauseType, operator:Clause|Self)->None:
        """
        Adds a clause to the current compound instance.

        Attributes:
        -----------------------
            - type:Literal["must", "mustNot", "should", "filter"] : The type of clause to add
            - statement:dict : The operator statement of the clause to add
        
        
        """

        if type == "must":
            self.must.append(operator)
        elif type == "mustNot":
            self.must_not.append(operator)
        elif type == "filter":
            self.filter.append(operator)
        elif type == "should":
            self.should.append(operator)

    #---------------------------------------------
    # Operators
    #---------------------------------------------
    def autocomplete(
            self,
            type:ClauseType,
            *,
            query:str|list[str], 
            path:str, 
            token_order:str="any",
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds an autocomplete clause to the current compound instance."""
        
        _autocomplete = Autocomplete(
            query=query,
            path=path,
            token_order=token_order,
            fuzzy=fuzzy,
            score=score
        )

        self._register_clause(type, _autocomplete)
    
        return self


    def compound(
            self, 
            type:ClauseType, 
            must:list["Clause|Compound"]=[],
            must_not:list["Clause|Compound"]=[],
            should:list["Clause|Compound"]=[],
            filter:list["Clause|Compound"]=[],
            minimum_should_match:int=0,
            **kwargs:Any
        )->Self:
        """Adds a compound clause to the current compound instance."""

        _compound = Compound(
            must=must,
            must_not=must_not,
            should=should,
            filter=filter,
            minimum_should_match=minimum_should_match
        )

        self._register_clause(type, _compound)

        return _compound


    def equals(
            self,
            type,
            path:str,
            value:str|int|float|bool|datetime,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds an equals clause to the current compound instance."""

        _equals = Equals(
            path=path,
            value=value,
            score=score
        ).statement

        self._register_clause(type, _equals)

        return self


    def exists(self, type:ClauseType, path:str, **kwargs:Any)->Self:
        """Adds an exists clause to the current compound instance."""

        _exists = Exists(path=path)
        self._register_clause(type, _exists)

        return self


    def more_like_this(self, type:ClauseType, like:dict|list[dict], **kwargs:Any)->Self:
        """Adds a more_like_this clause to the current compound instance."""

        _more_like_this = MoreLikeThis(like=like)
        self._register_clause(type, _more_like_this)

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
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds a range clause to the current compound instance."""

        _range = Range(
            path=path,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            score=score
        )

        self._register_clause(type, _range)

        return self


    def regex(
            self,
            type:ClauseType,
            *,
            query:str|list[str],
            path:str|list[str],
            allow_analyzed_field:bool=False,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds a regex clause to the current compound instance."""

        _regex = Regex(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )


        self._register_clause(type, _regex)

        return self


    def text(
            self,
            type:ClauseType,
            *,
            query:str|list[str],
            path:str|list[str],
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            synonyms:str|None=None,
            **kwargs:Any
    )->Self:
        """Adds a text clause to the current compound instance."""

        _text = Text(
            query=query,
            path=path,
            score=score,
            fuzzy=fuzzy,
            synonyms=synonyms
        )

        self._register_clause(type, _text)

        return self


    def wildcard(
            self,
            type:ClauseType,
            *,
            query:str|list[str],
            path:str|list[str],
            allow_analyzed_field:bool=False,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds a wildcard clause to the current compound instance."""

        _wildcard = Wildcard(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )

        self._register_clause(type, _wildcard)

        return self
    
    #---------------------------------------------
    # Clauses
    #---------------------------------------------
    def must_(
            self,
            operator_name:OperatorLiteral,
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            **kwargs
    )->Self:
        """Adds a must clause to the current compound instance."""
        
        kwargs.update(
            {
                "path":path,
                "query":query,
                "fuzzy":fuzzy,
                "score":score
            }
        )

        return self.__get_operators_map__(operator_name)("must", **kwargs)


    def must_not_(
            self,
            operator_name:OperatorLiteral,
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            **kwargs
    )->Self:
        """Adds a must_not clause to the current compound instance."""
        
        kwargs.update(
            {
                "path":path,
                "query":query,
                "fuzzy":fuzzy,
                "score":score
            }
        )

        return self.__get_operators_map__(operator_name)("mustNot", **kwargs)


    def should_(
            self,
            operator_name:OperatorLiteral,
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            **kwargs
    )->Self:
        """Adds a should clause to the current compound instance."""
        
        kwargs.update(
            {
                "path":path,
                "query":query,
                "fuzzy":fuzzy,
                "score":score
            }
        )

        return self.__get_operators_map__(operator_name)("should", **kwargs)


    def filter_(
            self,
            operator_name:OperatorLiteral,
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            **kwargs
    )->Self:
        """Adds a filter clause to the current compound instance."""
        
        kwargs.update(
            {
                "path":path,
                "query":query,
                "fuzzy":fuzzy,
                "score":score
            }
        )

        return self.__get_operators_map__(operator_name)("filter", **kwargs)

    #---------------------------------------------
    # Utility functions
    #---------------------------------------------
    def __get_operators_map__(self, operator_name:OperatorLiteral)->Callable[...,Self]:
        """Returns the operator class associated with the given operator name."""

        operators_map = {
            "autocomplete":self.autocomplete,
            "compound":self.compound, #FIXME : This breaks typing
            "equals":self.equals,
            "exists":self.exists,
            "range":self.range,
            "more_like_this":self.more_like_this,
            "regex":self.regex,
            "text":self.text,
            "wildcard":self.wildcard
        }

        return operators_map[operator_name]

if __name__ == "__main__":
    print(Compound())