"""
Module defining an interface to the facet collector

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 13/05/2023
Source : https://www.mongodb.com/docs/manual/meta/aggregation-quick-reference/

# Definition
# --------------------------------------------
The facet collector groups results by values or ranges in the specified faceted fields 
and returns the count for each of those groups.

You can use facet with both the $search and $searchMeta stages. 
MongoDB recommends using facet with the $searchMeta stage to retrieve metadata results only for the query. 
To retrieve metadata results and query results using the $search stage, you must use the $$SEARCH_META aggregation variable. 
See SEARCH_META Aggregation Variable to learn more.


# Syntax
# ----------------------------------------------
facet has the following syntax:

{
  "$searchMeta"|"$search": {
    "index": <index name>, // optional, defaults to "default"
    "facet": {
      "operator": {
        <operator-specifications>
      },
      "facets": {
        <facet-definitions>
      }
    }
  }
}

# Fields
----------------------------------------------
Field       Type            Description

facets      document        Defines the facets to return.

operator    document        Defines the operator to use to group the results.

# Facet Definition
----------------------------------------------
The facet definition document contains the facet name and options specific to a type of facet. 
Atlas Search supports the following types of facets:

    * String Facets
    * Numeric Facets
    * Date Facets

# String Facets

String facets allow you to narrow down Atlas Search results 
based on the most frequent string values in the specified string field. 
Note that the string field must be indexed as 
[How to Index String Fields For Faceted Search](https://www.mongodb.com/docs/atlas/atlas-search/field-types/string-facet-type/#std-label-bson-data-types-string-facet).

String facets have the following syntax:

    >>> {
            "$searchMeta": {
                "facet":{
                "operator": {
                    <operator-specification>
                },
                "facets": {
                    "<facet-name>" : {
                    "type" : "string",
                    "path" : "<field-path>",
                    "numBuckets" : <number-of-categories>,
                    }
                }
                }
            }
        }

# Numeric Facets

Numeric facets allow you to determine the frequency of numeric values in your search results 
by breaking the results into separate ranges of numbers.

Numeric facets have the following syntax:

    >>> {
            "$searchMeta": {
                "facet":{
                "operator": {
                    <operator-specification>
                },
                "facets": {
                    "<facet-name>" : {
                    "type" : "number",
                    "path" : "<field-path>",
                    "boundaries" : <array-of-numbers>,
                    "default": "<bucket-name>"
                    }
                }
                }
            }
        }

# Date Facets

Date facets allow you to narrow down search results based on a date.

    >>> {
            "$searchMeta": {
                "facet":{
                "operator": {
                    <operator-specification>
                },
                "facets": {
                    "<facet-name>" : {
                    "type" : "date",
                    "path" : "<field-path>",
                    "boundaries" : <array-of-dates>,
                    "default": "<bucket-name>"
                    }
                }
                }
            }
        }

# Facet Results
----------------------------------------------

For a facet query, Atlas Search returns a mapping of the defined facet names to an array of buckets for that facet in the results. 
The facet result document contains the buckets option, which is an array of resulting buckets for the facet. 
Each facet bucket document in the array has the following fields:

Option      Type            Description

_id         object          The value of the facet.
count       integer         The number of documents in the facet.


# SEARCH_META Aggregation Variable
----------------------------------------------

When you run your query using the $search stage, 
Atlas Search stores the metadata results in the $$SEARCH_META variable 
and returns only the search results. 
You can use the $$SEARCH_META variable in all the supported aggregation pipeline stages to view the metadata results for your $search query.

MongoDB recommends using the $$SEARCH_META variable only if you need both the search results and the metadata results. 
Otherwise, use the:

    * $search stage for just the search results.

    * $searchMeta stage for just the metadata results.

# Limitations
----------------------------------------------

The following limitations apply:

    * You can run facet queries on a single field only. You can't run facet queries on groups of fields.

    * You can run facet queries over sharded collections on clusters running MongoDB v6.0 only.


"""

from datetime import datetime
from typing import Any, Callable, Literal
from typing_extensions import Self

from monggregate.base import BaseModel, pyd
from monggregate.fields import FieldName
from monggregate.search.collectors.collector import SearchCollector
from monggregate.search.operators import(
    Autocomplete,
    Compound,
    Equals,
    Exists,
    MoreLikeThis,
    Range,
    Regex,
    Text,
    Wildcard,
    AnyOperator
)
from monggregate.search.operators.operator import OperatorLiteral
from monggregate.search.commons import FuzzyOptions

# Aliases
# ----------------------------------------------
FacetType = Literal['string', 'number', 'date']

# Strings
# ----------------------------------------------
class FacetName(FieldName):
    """
    Subclass of FieldName to represent a facet name
    
    Facets should refer to collctions fields that are indexed as facet fields.

    """

# Results
# ----------------------------------------------
class FacetBucket(BaseModel):
    """
    Represents a facet bucket.
    
    A facet bucket is an occurence (for categorical facets) or a range(for numeric facets) of a facet value in the search results.
    and the number of documents in the search results that have that facet value.

    """

    _id : str|int|float|datetime
    count : int


class FacetBuckets(BaseModel):
    """
    Represents the facet buckets for a facet.
    
    The facet result document contains the buckets option, 
    which is an array of resulting buckets for the facet.
    """

    buckets : list[FacetBucket]


FacetResult = dict[FacetName, FacetBuckets]


# Query
# ----------------------------------------------
class FacetDefinition(BaseModel):
    """
    Abstract base class for facet definitions
    
    Used to define StringFacet, NumericFacet and DateFacet which are classes defining the parameters
    used to define the facets that need to be computed in a search query.
    """

    path : str
    name : FacetName = ""
    

    @pyd.validator('name', pre=True, always=True)
    def set_name(cls, name: str, values:dict[str,str]) -> FacetName:
        """Sets the name from the field path"""

        path = values["path"]
        if not name:
            name = path # TODO : Maybe the path might need to be cleaned ? (., $, etc) <VM, 11/06/2023>

        return name
        

class StringFacet(FacetDefinition):
    """
    String facet definition
    
    Attributes
    -------------------------
        - type, Literal['string'] : facet type. Defaults to 'string' and has to be 'string'
        - path, str : path to the field to facet on
        - num_buckets, int : Maximum number of facet categories to return in the results. 
                             Value must be less than or equal to 1000. 
                             If specified, Atlas Search may return fewer categories than requested if the data is grouped into fewer categories than your requested number. 
                             If omitted, defaults to 10, which means that Atlas Search will return only the top 10 facet categories by count.
    
    """

    type : Literal['string'] = 'string'
    num_buckets : int = 10

    @property
    def statement(self) -> dict:
        
        return self.resolve({self.name : self.dict(by_alias=True, exclude={"name"})})


class NumericFacet(FacetDefinition):
    """
    Numeric facet definition

    Attributes
    -------------------------
        - type, Literal['number'] : facet type. Defaults to 'number' and has to be 'number'
        - path, str : path to the field to facet on
        - boundaries, list[int|float] : list of numeric values, in ascending order, that specify
                                              the boundaries for each bucket. You must specify at least two boundaries.
                                              Each adjacent pair of values acts aas the inclusive lower boundary and exclusive upper boundary for a bucket.
        - default, str : default bucket name to use for values that do not fall in any bucket
    
    """

    type : Literal['number'] = 'number'
    boundaries : list[int|float]
    default : str|None

    @property
    def statement(self) -> dict:
        
        return self.resolve({self.name : self.dict(by_alias=True, exclude={"name"})})


class DateFacet(FacetDefinition):
    """
    Numeric facet definition

    Attributes
    -------------------------
        - type, Literal['date'] : facet type. Defaults to 'date' and has to be 'date'
        - path, str : path to the field to facet on
        - boundaries, list[datetime] : list of datetime values, in ascending order, that specify

    """

    type : Literal['date'] = 'date'
    boundaries : list[datetime]
    default : str|None

    @property
    def statement(self) -> dict:
        
        return self.resolve({self.name : self.dict(by_alias=True, exclude={"name"})})

AnyFacet = StringFacet|NumericFacet|DateFacet
Facets = list[AnyFacet]

# Collector
# ----------------------------------------------
class Facet(SearchCollector):
    """
    Creates a facet query to be used in a search pipeline.

    Description
    -------------------------
    The facet collector groups results by values or ranges in the specified faceted fields 
    and returns the count for each of those groups.

    Attributes
    -------------------------
        - operator, dict|None : operator to use to combine the facet results with the search results.
        - facets, dict[FacetName, FacetDefinition] : dictionary of facet definitions to use in the facet query.
    
    """

    operator : AnyOperator|None
    facets : Facets = []


    @pyd.validator("facets")
    def validate_facets(cls, facets:Facets)->Facets:
        """
        Validates facets.
        Ensures the facets names are unique
        """

        names = []
        for facet in facets:
            names.append(facet.name)

        if len(facets) > len(set(names)):
            msg = "Some facets have identical names. Facet names must be unique."
            msg += "\n"
            msg += f"Facets names : {names}"
            raise ValueError(msg)
        
        return facets


    @property
    def statement(self) -> dict:

        if not self.facets:
            raise ValueError("No facets were defined")

        
        _statement = {
            "facet":{
                "facets":{}
            }
        }

        for facet in self.facets:
            _statement["facet"]["facets"].update(facet.statement)

        if self.operator:
            _statement["facet"].update({"operator":self.operator.statement})
        
        return self.resolve(_statement)
    
    #---------------------------------------------------------
    # Constructors
    #---------------------------------------------------------
    @classmethod
    def from_operator(
        cls, 
        operator_name:OperatorLiteral,
        path:str|list[str]|None=None,
        query:str|list[str]|None=None,
        fuzzy:FuzzyOptions|None=None,
        score:dict|None=None,
        **kwargs:Any)->Self:
        """Instantiates a search stage from a search operator"""

        kwargs.update(
            {
                "path":path,
                "query":query,
                "fuzzy":fuzzy,
                "score":score
            }
        )

        return cls.__get_constructors_map__(operator_name)(**kwargs)


    @classmethod
    def init_autocomplete(
        cls,
        query:str|list[str], 
        path:str, 
        token_order:str="any",
        fuzzy:FuzzyOptions|None=None,
        score:dict|None=None,
        **kwargs:Any)->Self:
        """
        Creates a search stage with an autocomplete operator
        
        Summary:
        -----------------------------
        This stage searches for a word or phrase that contains a sequence of characters from an incomplete input string.

        """


        _autocomplete = Autocomplete(
            query=query,
            path=path,
            token_order=token_order,
            fuzzy=fuzzy,
            score=score,
            **kwargs
        )

        return cls(operator=_autocomplete)
    

    @classmethod
    def init_compound(
        cls,
        minimum_should_clause:int=1,
        *,
        must : list[AnyOperator]=[],
        must_not : list[AnyOperator]=[],
        should : list[AnyOperator]=[],
        filter : list[AnyOperator]=[],
        **kwargs:Any
        
    )->Self:
        """xxxx"""
 

        _compound = Compound(
            must=must,
            must_not=must_not,
            should=should,
            filter=filter,
            minimum_should_clause=minimum_should_clause,
            **kwargs
        )

        return cls(operator=_compound)


    @classmethod
    def init_equals(
        cls,
        path:str,
        value:str|int|float|bool|datetime,
        score:dict|None=None,
        **kwargs:Any
        )->Self:
        """
        Creates a search stage with an equals operator

        Summary:
        --------------------------------
        This checks whether a field matches a value you specify.
        You may want to use this for filtering purposes post textual search.
        That is you may want to use it in a compound query or as, the second stage of your search.
        
        """

      
        _equals = Equals(
            path=path,
            value=value,
            score=score
        )

        return cls(operator=_equals)


    @classmethod
    def init_exists(cls, path:str, **kwargs:Any)->Self:
        """
        Creates a search stage with an exists operator

        Summary:
        --------------------------------
        This checks whether a field matches a value you specify.
        You may want to use this for filtering purposes post textual search.
        That is you may want to use it in a compound query or as, the second stage of your search.
        
        """


        _exists = Exists(path=path)

        return cls(operator=_exists)
    
    
    @classmethod
    def init_more_like_this(cls, like:dict|list[dict], **kwargs:Any)->Self:
        """
        Creates a search stage  with a more_like_this operator

        Summary:
        --------------------------------
        The moreLikeThis operator returns documents similar to input documents. 
        The moreLikeThis operator allows you to build features for your applications 
        that display similar or alternative results based on one or more given documents.

        """
        
      
        _more_like_this = MoreLikeThis(like=like)

        return cls(operator=_more_like_this)


    @classmethod
    def init_range(
        cls,
        path:str|list[str],
        gt:int|float|datetime|None=None,
        lt:int|float|datetime|None=None,
        gte:int|float|datetime|None=None,
        lte:int|float|datetime|None=None,
        score:dict|None=None,
        **kwargs:Any
    )->Self:
        """
        Creates a search stage with a range operator

        Summary:
        --------------------------------
        This checks whether a field value falls into a specific range
        You may want to use this for filtering purposes post textual search.
        That is you may want to use it in a compound query or as, the second stage of your search.
        
        
        """

        _range = Range(
            path=path,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            score=score
        )

        return cls(operator=_range)


    @classmethod
    def init_regex(
        cls,
        query:str|list[str],
        path:str|list[str],
        allow_analyzed_field:bool=False,
        score:dict|None=None,
        **kwargs:Any
    )->Self:
        """
        Creates a search stage with a regex operator.

        Summary:
        ----------------------------
        regex interprets the query field as a regular expression. regex is a term-level operator, meaning that the query field isn't analyzed (read processed).
        
        """

     
        _regex = Regex(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )

        return cls(operator=_regex)


    @classmethod
    def init_text(
        cls,
        query:str|list[str],
        path:str|list[str],
        fuzzy:FuzzyOptions|None=None,
        score:dict|None=None,
        synonyms:str|None=None,
        **kwargs:Any
    )->Self:
        """
        Creates a search stage with a text opertor

        Summary:
        ---------------------------------
        The text operator performs a full-text search using the analyzer that you specify in the index configuration. 
        If you omit an analyzer, the text operator uses the default standard analyzer.
        
        """


        _text = Text(
            query=query,
            path=path,
            score=score,
            fuzzy=fuzzy,
            synonyms=synonyms
        )

        return cls(operator=_text)


    @classmethod
    def init_wildcard(
        cls,
        query:str|list[str],
        path:str|list[str],
        allow_analyzed_field:bool=False,
        score:dict|None=None,
        **kwargs:Any
    )->Self:
        """
        Creates a search stage with a wildcard opertor

        Summary:
        ---------------------------------
        The wildcard operator enables queries which use special characters in the search string that can match any character.
        
        """

        
        _wilcard = Wildcard(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )

        return cls(operator=_wilcard)


    # ----------------------------------------------
    # Operators
    # ----------------------------------------------
    def autocomplete(
            self,
            *,
            query:str|list[str], 
            path:str, 
            token_order:str="any",
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds an autocomplete clause to the current facet instance."""
        
        _autocomplete = Autocomplete(
            query=query,
            path=path,
            token_order=token_order,
            fuzzy=fuzzy,
            score=score
        )

        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _autocomplete
        elif isinstance(self.operator, Compound):
            self.operator.autocomplete(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_autocomplete.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _autocomplete],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator

        return self
    
    def equals(
            self,
            path:str,
            value:str|int|float|bool|datetime,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds an equals clause to the current facet instance."""

        _equals = Equals(
            path=path,
            value=value,
            score=score
        )

        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _equals
        elif isinstance(self.operator, Compound):
            self.operator.equals(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_equals.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _equals],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator



        return self

    def exists(self, path:str, **kwargs:Any)->Self:
        """Adds an exists clause to the current facet instance."""

        _exists = Exists(path=path)
        
        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _exists
        elif isinstance(self.operator, Compound):
            self.operator.exists(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_exists.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _exists],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator


        return self
    
    def more_like_this(
            self,
            like:dict|list[dict],
            **kwargs:Any
    )->Self:
        """Adds a more_like_this clause to the current facet instance."""

        _more_like_this = MoreLikeThis(like=like)
        
        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _more_like_this
        elif isinstance(self.operator, Compound):
            self.operator.more_like_this(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_more_like_this.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _more_like_this],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator


        return self

    def range(
            self,
            *,
            path:str|list[str],
            gt:int|float|datetime|None=None,
            lt:int|float|datetime|None=None,
            gte:int|float|datetime|None=None,
            lte:int|float|datetime|None=None,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds a range clause to the current facet instance."""

        _range = Range(
            path=path,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            score=score
        )

        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _range
        elif isinstance(self.operator, Compound):
            self.operator.range(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_range.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _range],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator



        return self

    def regex(
            self,
            *,
            query:str|list[str],
            path:str|list[str],
            allow_analyzed_field:bool=False,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds a regex clause to the current facet instance."""

        _regex = Regex(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )

        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _regex
        elif isinstance(self.operator, Compound):
            self.operator.regex(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_regex.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _regex],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator


        return self

    def text(
            self,
            *,
            query:str|list[str],
            path:str|list[str],
            fuzzy:FuzzyOptions|None=None,
            score:dict|None=None,
            synonyms:str|None=None,
            **kwargs:Any
    )->Self:
        """Adds a text clause to the current facet instance."""

        _text = Text(
            query=query,
            path=path,
            score=score,
            fuzzy=fuzzy,
            synonyms=synonyms
        )

        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _text
        elif isinstance(self.operator, Compound):
            self.operator.text(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_text.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _text],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator



        return self

    def wildcard(
            self,
            *,
            query:str|list[str],
            path:str|list[str],
            allow_analyzed_field:bool=False,
            score:dict|None=None,
            **kwargs:Any
    )->Self:
        """Adds a wildcard clause to the current facet instance."""

        _wildcard = Wildcard(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )

        clause_type = kwargs.get("type", "should")
        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        if not self.operator:
            self.operator = _wildcard
        elif isinstance(self.operator, Compound):
            self.operator.wildcard(
                type=clause_type,
                minimum_should_match=minimum_should_match, 
                **_wildcard.dict())
        else:
            new_operator = Compound(
                should=[self.operator, _wildcard],
                minimum_should_match=minimum_should_match
                )
            self.operator = new_operator


        return self
    
    # ----------------------------------------------
    # Facets
    # ----------------------------------------------
    def facet(
            self,
            path:str,
            name:str|None=None,
            type:FacetType='string',
            num_buckets:int|None=None,
            boundaries:list[int|float]|list[datetime]|None=None,
            default:str|None=None,
            **kwargs:Any # NOTE : To prevent errors from passing extra argumentscf #100 on GitHub <VM, 22/01/2024>
    )->Self:
        
        if type=="string":
            if num_buckets is None:
                num_buckets = 10
            facet = StringFacet(
                name=name,
                path=path,
                num_buckets=num_buckets
            )
        elif type=="number":
            facet = NumericFacet(
                name=name,
                path=path,
                boundaries=boundaries,
                default=default
            )
        elif type=="date":
            facet = DateFacet(
                name=name,
                path=path,
                boundaries=boundaries,
                default=default
            )
        else:
            raise ValueError(f"Invalid facet type. Valid facet types are 'string', 'number' and 'date'. Got {type} instead.")

        self.facets.append(facet)

        return self

    def numeric(
            self,
            path:str,
            *,
            boundaries:list[int|float],
            name:str|None=None,
            default:str|None=None
    )->Self:
        """Adds a numeric facet to the current facet instance."""

        self.facet(
            type="number",
            path=path,
            name=name,
            boundaries=boundaries,
            default=default
        )
        return self
    
    def date(
            self,
            path:str,
            *,
            boundaries:list[datetime],
            name:str|None=None,
            default:str|None=None
    )->Self:
        """Adds a date facet to the current facet instance."""

        self.facet(
            type="date",
            path=path,
            name=name,
            boundaries=boundaries,
            default=default
        )
        return self
    
    def string(
            self,
            path:str,
            *,
            num_buckets:int=10,
            name:str|None=None
    )->Self:
        """Adds a string facet to the current facet instance."""

        self.facet(
            type="string",
            path=path,
            name=name,
            num_buckets=num_buckets
        )
        return self
    
    # ----------------------------------------------
    # Facet Interface
    # ----------------------------------------------
    @staticmethod
    def NumericFacet(
        *,
        path:str,
        name:FacetName|None=None,
        boundaries:list[int|float],
        default:str|None=None
    )->NumericFacet:
        """Returns a numeric facet instance."""

        return NumericFacet(
            name=name,
            path=path,
            boundaries=boundaries,
            default=default
        )
    
    @staticmethod
    def StringFacet(
        *,
        path:str,
        name:FacetName|None=None,
        num_buckets:int=10
    )->StringFacet:
        """Returns a string facet instance."""

        return StringFacet(
            name=name,
            path=path,
            num_buckets=num_buckets
        )
    
    @staticmethod
    def DateFacet(
        *,
        path:str,
        name:FacetName|None=None,
        boundaries:list[datetime],
        default:str|None=None
    )->DateFacet:
        """Returns a date facet instance."""

        return DateFacet(
            name=name,
            path=path,
            boundaries=boundaries,
            default=default
    )

    # TODO : Overload this method to make return type more precise.
    @staticmethod
    def Facet(
        *,
        type:Literal['string', 'number', 'date'],
        path:str,
        name:FacetName|None=None,
        num_buckets:int=10,
        boundaries:list[int|float]|list[datetime]|None=None,
        default:str|None=None
    )->AnyFacet:
        """Returns a facet instance."""

        if type=="string":
            facet = Facet.StringFacet(
                name=name,
                path=path,
                num_buckets=num_buckets
            )
        elif type=="number":
            facet = Facet.NumericFacet(
                name=name,
                path=path,
                boundaries=boundaries,
                default=default
            )
        else:
            facet = Facet.DateFacet(
                name=name,
                path=path,
                boundaries=boundaries,
                default=default
            )

        return facet

    # ----------------------------------------------
    # Utilities
    # ----------------------------------------------
    @classmethod
    def __get_constructors_map__(cls, operator_name:str)->Callable[...,Self]:
        """Returns appropriate constructor from operator name"""

        _constructors_map = {
            "autocomplete":cls.init_autocomplete,
            "compound":cls.init_compound,
            "equals":cls.init_equals,
            "exists":cls.init_exists,
            #"facet":cls.init_facet,
            "more_like_this":cls.init_more_like_this,
            "range":cls.init_range,
            "regex":cls.init_regex,
            "text":cls.init_text,
            "wildcard":cls.init_wildcard
        }

        return _constructors_map[operator_name]