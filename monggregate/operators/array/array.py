"""Base array operator module"""

# Standard Library Imports
# -----------------------------------------
from abc import ABC
from typing import Any

# Local imports
# -----------------------------------------
from monggregate.operators import Operator
from monggregate.utils import StrEnum

# Enums
# -----------------------------------------
class ArrayOperatorEnum(StrEnum):
    """Enumeration of available array operators"""


    ARRAY_ELEM_AT = "$arrayElemAt" # Returns the element at the specified array index.
    ARRAY_TO_OBJECT = "$arrayToObject" # Converts an array of key value pairs to a document.
    CONCAT_ARRAYS = "$concatArrays" # Concatenates arrays to return the concatenated array.
    FILTER = "$filter" # Selects a subset of the array to return an array with only the elements that match the filter condition.
    FIRST = "$first" # Returns the first array element. Distinct from $first accumulator.
    FIRST_N = "$firstN" # Returns a specified number of elements from the beginning of an array. Distinct from the $firstN accumulator.
    IN = "$in" # Returns a boolean indicating whether a specified value is in an array.
    INDEX_OF_ARRAY = "$indexOfArray" # Searches an array for an occurrence of a specified value and returns the array index of the first occurrence. If the substring is not found, returns -1.
    IS_ARRAY = "$isArray" # Determines if the operand is an array. Returns a boolean.
    LAST = "$last" #Returns the last array element. Distinct from $last accumulator.
    LAST_N = "$lastN" # Returns a specified number of elements from the end of an array. Distinct from the $lastN accumulator.
    MAP = "$map" # Applies a subexpression to each element of an array and returns the array of resulting values in order. Accepts named parameters.
    MAX_N = "$maxN" # Returns the n largest values in an array. Distinct from the $maxN accumulator.
    MIN_N = "$minN" # Returns the n smallest values in an array. Distinct from the $minN accumulator.
    OBJECT_TO_ARRAY = "$objectToArray" # Converts a document to an array of documents representing key-value pairs.
    RANGE = "$range" # Outputs an array containing a sequence of integers according to user-defined inputs.
    REDUCE = "$reduce" # Applies an expression to each element in an array and combines them into a single value.
    REVERSE_ARRAY = "$reverseArray" # Returns an array with the elements in reverse order.
    SIZE = "$size" # Returns the number of elements in the array. Accepts a single expression as argument.
    SLICE = "$slice" # Returns a subset of an array.
    SORT_ARRAY = "$sortArray" # Sorts the elements of an array.
    ZIP = "$zip" # Merge two arrays together.


# Classes
# -----------------------------------------
class ArrayOperator(Operator, ABC):
    """Base class for array operators"""


class ArrayOnlyOperator(ArrayOperator, ABC):
    """Base class for array operators that work directly on the input array without any other parameters"""

    expression : Any

# Type aliases
# -----------------------------------------
ArrayOperatorExpression = dict[ArrayOperatorEnum, Any]
