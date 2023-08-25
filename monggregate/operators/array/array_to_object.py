"""
Module defining an interface to $arrayToObject operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------

Last Updated (in this package) : 12/11/2022
Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/arrayToObject/#mongodb-expression-exp.-arrayToObject


Definition
----------------------------------------
Converts an array into a single document; the array must be either:

    * An array of two-element arrays where the first element is the field name,
      and the second element is the field value:

    >>> [ [ "item", "abc123"], [ "qty", 25 ] ]

- OR -

    * An array of documents that contains two fields, k and v where:

        * The k field contains the field name.

        * The v field contains the value of the field.

    >>> [ { "k": "item", "v": "abc123"}, { "k": "qty", "v": 25 } ]

$arrayToObjecthas the following syntax:

    >>> { $arrayToObject: <expression> }

The <expression> can be any valid expression that that resolves to an array of two-element arrays or array of documents that contains "k" and "v" fields.

Behavior
------------------------------
If the name of a field repeats in the array,

    * Starting in 4.0.5, $arrayToObject uses the last value for that field.
      For 4.0.0-4.0.4, the value used depends on the driver.

    * Starting in 3.6.10, $arrayToObject uses the last value for that field.
      For 3.6.0-3.6.9, the value used depends on the driver.

    * Starting in 3.4.19, $arrayToObject uses the last value for that field.
      For 3.4.0-3.4.19, the value uses depends on the driver.

"""

from typing import Any
from monggregate.operators.array.array import ArrayOperator

class ArrayToObject(ArrayOperator):
    """
    Creates an $arrayToObject expression

    Attributes
    ----------------------
        - expression, Expression : Any valid expression that resolves to an array of two-element arrays
                                   or array if documents that contains "k" and "v" fields.


    """

    expression : Any


    @property
    def statement(self) -> dict:
        return self.resolve({
            "$arrayToObject" : self.expression
        })

def array_to_object(expression:Any)->ArrayToObject:
    """Returns a $arrayToObject operator"""

    return ArrayToObject(expression=expression)
