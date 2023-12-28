"""Array Operators subpackage"""

from monggregate.operators.array.first import First, first
from monggregate.operators.array.last import Last, last
from monggregate.operators.array.array_to_object import ArrayToObject, array_to_object
from monggregate.operators.array.filter import Filter, filter # pylint: disable=redefined-builtin
from monggregate.operators.array.in_ import In, in_
from monggregate.operators.array.is_array import IsArray, is_array
from monggregate.operators.array.max_n import MaxN, max_n
from monggregate.operators.array.min_n import MinN, min_n
from monggregate.operators.array.size import Size, size
from monggregate.operators.array.sort_array import SortArray, sort_array

# TODO:
# * $arrayElemAt
# * $concatArrays
# * $indexOfArray
# * $map
# * $maxN
# * $minN
# * $objectToArray
# * $range
# * $reduce
# * $reverseArray
# * $slice
# * $zip