"""
Module defining an interface to $objectToArray operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/objectToArray/#mongodb-expression-exp.-objectToArray

Definition
-------------------
$objectToArray
Converts a document to an array. The return array contains an element for each field/value pair in the original document. Each element in the return array is a document that contains two fields k and v:

    * The k field contains the field name in the original document.

    * The v field contains the value of the field in the original document.

$objectToArray has the following syntax:

    >>> { $objectToArray: <object> }

The <object> expression can be any valid expression as long as it resolves to a document object.
$objectToArray applies to the top-level fields of its argument. If the argument is a document that itself contains embedded document fields, the
$objectToArray does not recursively apply to the embedded document fields.

For more information on expressions, see Expressions.

"""

from monggregate.operators.array.array import ArrayOperator
from typing import Any

class ObjectToArray(ArrayOperator):
    """
    Creates an $arrayToObject expression

    Attributes
    -------------------
        - expression, Expression : Any valid expression that resolves to an object

    """

    expression : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$objectToArray" : self.expression
        })

def object_to_array(expression:Any)->ObjectToArray:
    """Returns a $objectToArray operator"""

    return ObjectToArray(expression=expression)
