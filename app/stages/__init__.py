"""Stage Sub-package"""

from app.stages.match import Match
from app.stages.project import Project
from app.stages.count import Count
from app.stages.group import Group
from app.stages.replace_root import ReplaceRoot
from app.stages.set import Set
from app.stages.unwind import Unwind
from app.stages.sort import Sort
from app.stages.limit import Limit
from app.stages.sample import Sample
from app.stages.skip import Skip


# Aliases
# ---------------------------------
AddFields = Set
ReplaceWith = ReplaceRoot
