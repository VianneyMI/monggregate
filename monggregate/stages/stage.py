"""Stage Module"""

# Standard Library imports
#----------------------------
from abc import ABC

# Package imports
# ---------------------------
from monggregate.base import BaseModel
from monggregate.utils import StrEnum


class Stage(BaseModel, ABC):
    """MongoDB pipeline stage interface base class"""


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
