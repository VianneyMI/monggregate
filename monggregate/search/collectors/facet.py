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
from typing import Literal

from pydantic import Field, validator

from monggregate.base import BaseModel
from monggregate.expressions.fields import FieldName
from monggregate.search.collectors.collector import SearchCollector

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
    name : FacetName
    # TODO : Make name optional and copy path in it when not provided <VM, 17/05/2023>
    

# TODO : Maybe include a facet name in the below classes <VM, 14/05/2023>
# TODO : Define statements for the below classes
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
    num_buckets : int = Field(10, alias='numBuckets')

    @property
    def statement(self) -> dict:
        
        return {self.name : self.dict(by_alias=True)}


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
        
        return {self.name : self.dict(by_alias=True)}

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
    default : str

    @property
    def statement(self) -> dict:
        
        return {self.name : self.dict(by_alias=True)}

Facets = list[NumericFacet|DateFacet|StringFacet]

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

    operator : dict|None
    facets : Facets|list[dict]

    # FIXME : The below validator will be usable only when the automatic conversion to statement is deprecated <VM, 20/05/2023>
    # @validator("facets")
    # def validate_facets(cls, facets:Facets)->Facets:
    #     """
    #     Validates facets.
    #     Ensures the facets names are unique
    #     """

    #     names = set()
    #     for facet in facets:
    #         names.add(facet.name)

    #     if len(facets) > len(names):
    #         raise ValueError("Some facets have identical names")
        
    #     return facets


    @property
    def statement(self) -> dict:

        
        _statement = {
            "facets":{}
        }

        # FIXME : The below will work only when change is made to not express objects as dict statement automatically
        # <VM, 16/05/2023>
        for facet in self.facets:
            _statement["facets"].update(facet.statement)

        if self.operator:
            _statement["operator"] = self.operator
        
        return _statement
    
    # TODO : pipelinize this class for both operators and facet definitions
    