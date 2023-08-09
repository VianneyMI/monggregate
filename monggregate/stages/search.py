"""Module definining an interface to MongoDB $search stage operation in aggregation pipeline.

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------

Last Updated (in this package) : 25/04/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/query-syntax/#mongodb-pipeline-pipe.-search

# Definition
#---------------------------
The $search stage performs a full-text search on the specified field or fields which must be covered by an Atlas Search index.

$search
A $search pipeline stage has the following prototype form:

    >>> {
            $search: {
                "index": "<index-name>",
                "<operator-name>"|"<collector-name>": {
                <operator-specification>|<collector-specification>
                },
                "highlight": {
                <highlight-options>
                },
                "count": {
                <count-options>
                },
                "returnStoredSource": true | false
            }
        }

# Fields
#---------------------------

The $search stage takes a document with the following fields

Field                       Type       Necessity       Description

<collector-name>            document   Conditional     Name of the collector to use with the query. 
                                                       You can provide a document that contains the collector-specific options as the value for this field. 
                                                       Either this or <operator-name> is required.
count                       document   Optional        Document that specifies the count options for retrieving a count of the results. 
                                                       To learn more, see Count Atlas Search Results.
highlight                   document   Optional        Document that specifies the highlight options for displaying search terms in their original context.
index                       string     Required        Name of the Atlas Search index to use. If omitted, defaults to default
<operator-name>             document   Conditional     Name of the operator to search with. 
                                                       You can provide a document that contains the operator-specific options as the value for this field. 
                                                       Either this or <collector-name> is required.
returnStoredSource          boolean    Optional        Flag that specifies whether to perform a full document lookup on the backend database or return only stored source fields directly from Atlas Search. 
                                                       If omitted, defaults to false. To learn more, see Return Stored Source pyd.Fields.

# Behavior
#---------------------------
$search must be the first stage of any pipeline it appears in. 
$search cannot be used in:

    * a view definition

    * a $facet pipeline stage

# Aggregation Variable
#---------------------------
$search returns only the results of your query. The metadata results of your 
$search query are saved in the $$SEARCH_META aggregation variable. You can use the $$SEARCH_META variable to view the metadata results for your 
$search query. The $$SEARCH_META aggregation variable can be used anywhere after a 
$search stage in any pipeline, but it can't be used after the $lookup or $unionWith stage in any pipeline. 
The $$SEARCH_META aggregation variable can't be used in any subsequent stage after a $searchMeta stage.
                                                       
"""

from datetime import datetime
from typing import Any, Callable, Literal
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
    
from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.search.collectors import Facet, Facets
from monggregate.search.operators import(
    Autocomplete,
    Compound,
    Equals,
    Exists,
    MoreLikeThis,
    Range,
    Regex,
    Text,
    Wilcard,
    AnyOperator
)
from monggregate.search.commons import FuzzyOptions

# Enums
# -----------------------------------------------------
OperatorLiteral = Literal[
    "autocomplete",
    "equals",
    "exists",
    "facet",
    "more_like_this",
    "range",
    "regex",
    "text",
    "wildcard"
]

# Classes
# -----------------------------------------------------
class SearchBase(Stage):
    """Internals"""

    index : str = "default"
    count : dict|None
    highlight : dict|None
    return_stored_source : bool = pyd.Field(False, alias="returnStoredSource")
    score_details : bool = pyd.Field(False, alias="scoreDetails")

    @property
    def statement(self) -> dict[str, dict]:
    
        config = {
                "index":self.index,
                "highlight":self.highlight,
                "count":self.count,
                "returnStoredSource":self.return_stored_source,
                "scoreDetails":self.score_details
            }
        
     
        _statement = {
            "$search":config
        }
     
        return self.resolve(_statement)


class Search(SearchBase):
    """"
    Creates a $search statement in an aggregation pipeline

    Descrtiption
    -----------------------
    The $search stage performs a full-text search on the specified field or fields 
    which must be covered by an Atlas Search index.

    Attributes:
    -----------------------
        - index, str : name of the Atlas Search index to use. Defaults to default.

        - count, dict|None : Document that specifies the count options for retrieving a count
                             of the results. 

        - highlight, dict|None : Document that specifies the highlight options for displaying
                                 search terms in their original context.

        - return_stored_source, bool : Flag that specifies whether to perform a full document lookup
                                       on the backend database (mongod) or return only stored source fields
                                       directly from Atlas Search. Defaults to false.

        - score_details, bool : Flag that specifies whether to retrieve a detailed breakdown of
                                the score for the documents in the results. Defaults to false
                                To view the details, you must use the $meta expression in the
                                $project stage.

        - <operator-name>, dict|None : Name of the operator to search with. You can provide a document
                                  that contains the operator-specific options as the value for this field
                                  Either this or <collector-name> is required.

        - <collector-name>, dict|None : Name of the collector to use with the query. You can provide
                                        a document that contains the collector-specific options as the value
                                        for this field. Either this or <operator-name> is required.

    """

    
    collector : Facet|None
    operator : AnyOperator|None
    

    @pyd.validator("operator", pre=True, always=True)
    @classmethod
    def validate_operator(cls, value:dict, values:dict)->dict|None:
        """Ensures that either collector or operator is provided"""

        collector = values.get("collector")

        if collector is None and value is None:
            raise TypeError("Either collector or operator must be provided")
        elif collector and value:
            raise TypeError("Only one of collector or operator can be provided")
        
        return value
    
    @property
    def statement(self) -> dict[str, dict]:
    
        config = {
                "index":self.index,
                "highlight":self.highlight,
                "count":self.count,
                "returnStoredSource":self.return_stored_source,
                "scoreDetails":self.score_details
            }
        
        method = self.collector or self.operator

        config.update(method.statement)

        _statement = {
            "$search":config
        }
     
        return self.resolve(_statement)
    

    #---------------------------------------------------------
    # Constructors
    #---------------------------------------------------------
    @classmethod
    def __get_constructors_map__(cls, operator_name:str)->Callable:
        """Returns appropriate constructor from operator name"""

        _constructors_map = {
            "autocomplete":cls.autocomplete,
            "compound":cls.compound,
            "equals":cls.equals,
            "exists":cls.exists,
            "facet":cls.facet,
            "more_like_this":cls.more_like_this,
            "range":cls.range,
            "regex":cls.regex,
            "text":cls.text,
            "wildcard":cls.wildcard
        }

        return _constructors_map[operator_name]
    

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

        # FIXME : This could lead in duplicated arguments in kwargs <VM, 02/05/2023>
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
    def autocomplete(
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

        base_params = SearchBase(**kwargs).dict()
        cls.__reduce_kwargs(kwargs)

        autocomplete_statement = Autocomplete(
            query=query,
            path=path,
            token_order=token_order,
            fuzzy=fuzzy,
            score=score,
            **kwargs
        )

        return cls(**base_params, operator=autocomplete_statement)
    
    @classmethod
    def compound(
        cls,
        minimum_should_clause:int=1,
        *,
        must : list[dict]=[],
        must_not : list[dict]=[],
        should : list[dict]=[],
        filter : list[dict]=[],
        **kwargs:Any
        
    )->Self:

        base_params = SearchBase(**kwargs).dict()
        cls.__reduce_kwargs(kwargs)

        compound_statement = Compound(
            must=must,
            must_not=must_not,
            should=should,
            filter=filter,
            minimum_should_clause=minimum_should_clause,
            **kwargs
        )

        return cls(**base_params, operator=compound_statement)

    @classmethod
    def equals(
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

        base_params = SearchBase(**kwargs).dict()
        equals_statement = Equals(
            path=path,
            value=value,
            score=score
        )

        return cls(**base_params, operator=equals_statement)

    @classmethod
    def exists(cls, path:str, **kwargs:Any)->Self:
        """
        Creates a search stage with an exists operator

        Summary:
        --------------------------------
        This checks whether a field matches a value you specify.
        You may want to use this for filtering purposes post textual search.
        That is you may want to use it in a compound query or as, the second stage of your search.
        
        """

        base_params = SearchBase(**kwargs).dict()
        exists_statement = Exists(path=path)

        return cls(**base_params, operator=exists_statement)
    
    @classmethod
    def facet(cls, **kwargs:Any)->Self:
        """
        Creates a search stage with a facet operator

        Summary:
        --------------------------------

        """
        
        base_params = SearchBase(**kwargs).dict()
        cls.__reduce_kwargs(kwargs)
        
        operator = kwargs.pop("operator", None)
        facet_ = Facet(operator=operator, **kwargs)

        return cls(**base_params, collector=facet_)
    
    @classmethod
    def more_like_this(cls, like:dict|list[dict], **kwargs:Any)->Self:
        """
        Creates a search stage  with a more_like_this operator

        Summary:
        --------------------------------
        The moreLikeThis operator returns documents similar to input documents. 
        The moreLikeThis operator allows you to build features for your applications 
        that display similar or alternative results based on one or more given documents.

        """
        
        base_params = SearchBase(**kwargs).dict()
        more_like_this_stasement = MoreLikeThis(like=like)

        return cls(**base_params, operator=more_like_this_stasement)

    @classmethod
    def range(
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

        base_params = SearchBase(**kwargs).dict()
        range_statement = Range(
            path=path,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            score=score
        )

        return cls(**base_params, operator=range_statement)

    @classmethod
    def regex(
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

        base_params = SearchBase(**kwargs).dict()
        regex_statement = Regex(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )

        return cls(**base_params, operator=regex_statement)



    @classmethod
    def text(
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

        base_params = SearchBase(**kwargs).dict()
        cls.__reduce_kwargs(kwargs)

        text_statement = Text(
            query=query,
            path=path,
            score=score,
            fuzzy=fuzzy,
            synonyms=synonyms
        )

        return cls(**base_params, operator=text_statement)

    @classmethod
    def wildcard(
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

        base_params = SearchBase(**kwargs).dict()
        cls.__reduce_kwargs(kwargs)
        
        wilcard_statement = Wilcard(
            query=query,
            path=path,
            allow_analyzed_field=allow_analyzed_field,
            score=score
        )

        return cls(**base_params, operator=wilcard_statement)
    
    @classmethod
    def __reduce_kwargs(cls, kwargs:dict)->None:
        """
        Parses kwargs arguments to avoid passing arguments twice
        
        In particular removes SearchBase arguments from kwargs:
            - index, 
            - count, 
            - highlight, 
            - return_stored_source, 
            - score_details
        
        """

        kwargs.pop("index", None)
        kwargs.pop("count", None)
        kwargs.pop("highlight", None)
        kwargs.pop("return_stored_source", None)
        kwargs.pop("score_details", None)

# TODO : pipelinize Search class
# Instead of setting the search operator as a classmethods constructors
# transform them into chainable instance methods using the compound operator to combined the chained operations

#or offer both options by poviding init_<operator-name> and def <operator-name> methods