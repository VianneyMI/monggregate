"""Stage Sub-package"""

from monggregate.stages.stage import Stage
from monggregate.stages.bucket_auto import BucketAuto, GranularityEnum
from monggregate.stages.bucket import Bucket
from monggregate.stages.count import Count
from monggregate.stages.group import Group
from monggregate.stages.limit import Limit
from monggregate.stages.lookup import Lookup
from monggregate.stages.match import Match
from monggregate.stages.out import Out
from monggregate.stages.project import Project
from monggregate.stages.replace_root import ReplaceRoot
from monggregate.stages.sample import Sample
from monggregate.stages.search import Search
from monggregate.stages.search_meta import SearchMeta
from monggregate.stages.set import Set
from monggregate.stages.skip import Skip
from monggregate.stages.sort_by_count import SortByCount
from monggregate.stages.sort import Sort
from monggregate.stages.union_with import UnionWith
from monggregate.stages.unwind import Unwind
from monggregate.stages.unset import Unset



# TODO : Add the greater than 0 constraints on the models <VM, 18/09/2022>
# TODO : Add skipped links in documentation <VM, 18/09/2022>
# TODO : Add skipped notes or remove the useless ones
# TODO : Uniformize docstrings
#           - follow the same standard for code example (raw MongoDB example or example transformed in python dictionary)
# TODO : Replace links by markdown links when/where relevant <VM, 21/09/2022>
# TODO : Use #, ## or ### where relevant to create subsections <VM, 23/09/2022>
# TODO : When handling the aliases ensure to set the appropriate variable in the values in the root pyd.validators <VM, 26/09/2022>
# TODO : Validates field paths (they need to start with $) when relevant. Ex: In the BucketAuto stage, by should start with $ when it is a field path.


# Aliases
# ---------------------------------

    # MongoDB Official aliases
AddFields = Set
ReplaceWith = ReplaceRoot

    # Custom aliases
Explode = Unwind # to match pandas equivalent operation
