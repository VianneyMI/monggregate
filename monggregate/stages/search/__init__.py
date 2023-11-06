"""Search stages subpackage.

Contains search and search_meta modules.

"""
from typing import Literal

from monggregate.stages.search.search import Search
from monggregate.stages.search.search_meta import SearchMeta

SearchStageMap:dict[
    Literal["search", "searchMeta"],
    type[Search]|type[SearchMeta]
] = {
    "search":Search,
    "searchMeta":SearchMeta
}
