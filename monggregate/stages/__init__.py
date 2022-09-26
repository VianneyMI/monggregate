"""Stage Sub-package"""

from app.stages.stage import Stage
from app.stages.bucket_auto import BucketAuto
from app.stages.bucket import Bucket
from app.stages.count import Count
from app.stages.group import Group
from app.stages.limit import Limit
from app.stages.lookup import Lookup
from app.stages.match import Match
from app.stages.out import Out
from app.stages.project import Project
from app.stages.replace_root import ReplaceRoot
from app.stages.sample import Sample
from app.stages.set import Set
from app.stages.skip import Skip
from app.stages.sort_by_count import SortByCount
from app.stages.sort import Sort
from app.stages.unwind import Unwind


# TODO : Add the greater than 0 constraints on the models <VM, 18/09/2022>
# TODO : Add skipped links in documentation <VM, 18/09/2022>
# TODO : Add skipped notes or remove the useless ones
# TODO : Uniformize docstrings
#           - follow the same standard for code example (raw MongoDB example or example transformed in python dictionary)
# TODO : Replace links by markdown links when/where relevant <VM, 21/09/2022>
# TODO : Use #, ## or ### where relevant to create subsections <VM, 23/09/2022>


# Aliases
# ---------------------------------

    # MongoDB Official aliases
AddFields = Set
ReplaceWith = ReplaceRoot

    # Custom aliases
Explode = Unwind # to match pandas equivalent operation
