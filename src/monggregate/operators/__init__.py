"""Operators Sub-package"""

# pylint: disable=redefined-builtin
from monggregate.operators.operator import Operator

from monggregate.operators.accumulators import(
    Average, Avg, average, avg,
    Count, count,
    First, first,
    Last, last,
    Max, max,
    Min, min,
    Push, push,
    Sum, sum
)

from monggregate.operators.array import(
    ArrayToObject, array_to_object,
    Filter, filter,
#    First, first, #Commented as the array operator has the same name, syntax and does the same thing
    In, in_,
    IsArray, is_array,
#    Last, last,  #Commented as the array operator has the same name, syntax and does the same thing
    MaxN, max_n,
    MinN, min_n,
    Size, size,
    SortArray, sort_array
)

from monggregate.operators.boolean import(
    And, and_,
    Not, not_,
    Or, or_
)

from monggregate.operators.comparison import(
    Compare, Cmp, compare, cmp,
    Equal, Eq, equal, eq,
    GreatherThan, Gt, greather_than, gt,
    GreatherThanOrEqual, Gte, grether_than_or_equal, gte,
    LowerThan, Lt, lower_than, lt,
    LowerThanOrEqual, Lte, lower_than_or_equal, lte,
    NotEqual, Ne, not_equal, ne
)

from monggregate.operators.objects import(
    MergeObjects, merge_objects,
    ObjectToArray, object_to_array
)

from monggregate.operators.type_ import type_