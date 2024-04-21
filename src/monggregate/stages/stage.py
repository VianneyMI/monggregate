"""Stage Module"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod


# Package imports
# ---------------------------
from monggregate.base import BaseModel, Expression
from monggregate.utils import StrEnum


class Stage(BaseModel, ABC):
    """MongoDB pipeline stage interface base class"""

    @abstractmethod
    def to_expression(self)->Expression:
        """Converts an instance of a class inheriting from BaseModel to an expression"""

        return self.express(self)

    
    def __call__(self)->Expression:
        """Makes an instance of any class inheriting from this class callable"""

        return self.to_expression()


class StageEnum(StrEnum):
    """Enumeration of the available stages"""

    ADD_FIELDS = "$addFields"
    BUCKET = "$bucket"
    BUCKET_AUTO = "$bucket_auto"
    CHANGE_STREAM = "$changeStream"
    COLL_STATS = "$collStats"
    COUNT = "$count"
    DENSIFY = "$densify"
    DOCUMENTS = "$documents"
    FACET = "$facet"
    FILL = "$fill"
    GEO_NEAR = "$geoNear"
    GRAPH_LOOKUP = "$graphLookup"
    GROUP = "$group"
    INDEX_STATS = "$indexStats"
    LIMIT = "$limit"
    LIST_SESSIONS = "$listSessions"
    LOOKUP = "$lookup"
    MATCH = "$match"
    MERGE = "$merge"
    OUT = "$out"
    PLAN_CACHE_STATS = "$planCacheStats"
    PROJECT = "$project"
    REDACT = "$redact"
    REPLACE_ROOT = "$replaceRoot"
    REPLACE_WITH = "$replaceWith"
    SAMPLE = "$sample"
    SEARCH = "$search"
    SEARCH_META = "$searchMeta"
    SET = "$set"
    SET_WINDOW_FIELDS = "$setWindowFields"
    SKIP = "$skip"
    SORT = "$sort"
    SORT_BY_COUNT = "$sortByCount"
    UNION_WITH = "$unionWith"
    UNSET = "$unset"
    UNWIND = "$unwind"
