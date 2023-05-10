"""Module defining an interface to the facet collector"""

from datetime import datetime
from typing import Literal

from pydantic import Field

from monggregate.base import BaseModel
from monggregate.expressions.fields import FieldName
from monggregate.search.collectors.collector import SearchCollector

class FacetName(FieldName):
    """xxx"""

class FacetDefinition(BaseModel):
    """xxx"""

class StringFacet(FacetDefinition):
    """xxx"""

    type : Literal['string'] = 'string'
    path : str
    num_buckets : int = Field(10, alias='numBuckets')


class NumericFacet(FacetDefinition):
    """xxx"""

    type : Literal['number'] = 'number'
    path : str
    boundaries : list[int]|list[float]
    default : str

class DateFacet(FacetDefinition):
    """xxx"""

    type : Literal['date'] = 'date'
    path : str
    boundaries : list[datetime]
    default : str


class FacetCount(BaseModel):
    """xxx"""

    _id : str|int|float|datetime
    count : int


class FacetBuckets(BaseModel):
    """xxx"""

    buckets : list[FacetCount]


FacetResult = dict[FacetName, FacetBuckets]


class Facet(SearchCollector):
    """xxx"""

    operator : dict
    facets : dict[FacetName, FacetDefinition]