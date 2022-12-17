"""Base accumulator module"""

from abc import ABC

from monggregate.operators import Operator
from monggregate.utils import StrEnum

class Accumulator(Operator, ABC):
    """Base class for accumulators"""

class AccumulatorEnum(StrEnum):
    """Enumeration of available accumulators"""

    ACCUMULATOR ="$accumulator"
    ADD_TO_SET = "$addToSet"
    AVG = "$avg"
    BOTTOM = "$bottom"
    BOTTOM_N = "$bottomN"
    COUNT = "$count"
    FIRST = "$first"
    FIRST_N = "$firstN"
    LAST = "$last"
    LAST_N = "$lastN"
    MAX = "$max"
    MAX_N = "$maxN"
    MERGE_OBJECTS = "$mergeObjects"
    MIN = "$min"
    PUSH = "$push"
    STD_DEV_POP = "$stdDevPop"
    STD_DEV_SAMP = "$stdDevSamp"
    SUM = "$sum"
    TOP = "$top"
    TOP_N = "$topN"
