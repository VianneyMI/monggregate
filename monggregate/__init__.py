"""App Package"""

from monggregate.pipeline import Pipeline
from monggregate.stages import(
    Stage,
    AddFields,
    BucketAuto,
    Bucket,
    Count,
    Explode,
    Group,
    Limit,
    Lookup,
    Match,
    Out,
    Project,
    ReplaceWith,
    ReplaceRoot,
    Sample,
    Set,
    Skip,
    SortByCount,
    Sort,
    Unwind
)
from monggregate import expressions

# IMPORTANT : Please think about updated the pyproject.toml file when changing the version here.
__version__ = "0.7.0"
__author__ = "Vianney Mixtur"
__contact__ = "vianney.mixtur@outlook.fr"
__copyright__ = "TBD" # TODO : Explore this <VM, 26/09/2022>
__license__ = "MIT"

# Standard Library imports
#----------------------------

# 3rd Party imports
# ---------------------------

# Package imports
# ---------------------------
