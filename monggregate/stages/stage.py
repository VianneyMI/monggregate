"""Stage Module"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel, BaseConfig

# Package imports
# ---------------------------
from monggregate.utils import StrEnum

# NOTE : Stage should be an abstract base class and all operators should be classes inheriting from the base class
class Stage(BaseModel, ABC):
    """MongoDB pipeline stage interface bas class"""

    @property
    @abstractmethod
    def statement(self)->dict:
        """stage stament"""

        # this is a lazy attribute
        # what is currently in generate statement should go in here
        # TODO : Implement cache

    class Config(BaseConfig):
        """Configuration for Stage classes"""

        allow_population_by_field_name = True
        underscore_attrs_are_private = True

    def __call__(self)->dict:
        """Makes an instance of stage callable"""

        return self.statement

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
