"""
Module defining an interface to $sortArray operator


Online MongoDB documentation:
--------------------------------------------------------------------------------------

Last Updated (in this package) : 12/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sortArray/#mongodb-expression-exp.-sortArray

Definition
-----------------------------
New in version 5.2.

Sorts an array based on its elements. The sort order is user specified.

$sortArray has the following syntax:

    >>> $sortArray: {
        input: <array>,
        sortBy: <sort spec>
    }

        Field       Type        Description

    *   input       Expression  The array to be sorted.
                                The result is null if the expression
                                    * is missing
                                    * evaluates to null
                                    * evaluates to undefined
    *   sortBy      document    The document specifies a sort ordering

Behavior
---------------------------------
The $sortArray expression orders the input array according to the sortBy specification.

The $sortArray syntax and semantics are the same as the behavior in a $push operation modified by $sort

Sort by Document pyd.Fields

If the array elements are documents, you can sort by a document field.
Specify the field name and a sort direction, ascending (1), or descending (-1 ).

    >>> {
        input: <array-of-documents>,
        sortBy: { <document-field>: {sort-direction> }
    }

Sort by Value

To sort the whole array by value, or to sort by array elements that are not documents,
identify the input array and specify 1 for an ascending sort or -1 for descending sort in the sortBy parameter.

    >>> {
        input: <array-of-documents>,
        sortBy: { sort-direction> }
    }

Considerations

    * There is no implicit array traversal on the sort key.

    * Positional operators are not supported.
      A field name like "values.1" denotes a sub-field called "1" in the values array.
      It does not refer to the item at index 1 in the values array.

    * When a whole array is sorted, the sort is lexicographic.
      The aggregation $sort stage, behaves differently.
      See $sort for more details.

    * When an array is sorted by a field,
      any documents or scalars that do not have the specified field are sorted equally.
      The resulting sort order is undefined.

    * null values and missing values sort equally.

Sort Stability

The stability of the sort is not specified. Users should not rely on
$sortArray to use a particular sorting algorithm.

"""

from typing import Any, Literal

from monggregate.base import pyd
from monggregate.operators.array.array import ArrayOperator

class SortArray(ArrayOperator):
    """
    Creates a $sortArray expression

    Attributes
    --------------------------
        - expression, Expression : Any valid expression that resolves to an array
        - by, dict[str, Literal[1, -1]] :  document indicating a sort order
    """

    expression : Any = pyd.Field(alias="input")
    by : dict[str, Literal[1, -1]] = pyd.Field(1, alias="sort_by")

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$sortArray":{
                "input" : self.expression,
                "sortBy" : self.by
            }
        })

def sort_array(expression:Any, sort_by:dict[str, Literal[1, -1]])->SortArray:
    """Returns a $first operator"""

    return SortArray(
        expression = expression,
        sort_by = sort_by
    )
