"""
Module defining an interface to the $type operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/type/#mongodb-expression-exp.-type

Definition
-------------------
$type
Returns a string that specifies the BSON type of the argument.

$type has the following operator expression syntax:

    >>> { $type: <expression> }

The argument can be any valid expression.

Behavior
-------------------

Unlike the $type query operator, which matches array elements based on their BSON type, 
the $type aggregation operator does not examine array elements. 
Instead, when passed an array as its argument, the $type aggregation operator returns the type of the argument, i.e. "array".

If the argument is a field that is missing in the input document, $type returns the string "missing".

The following table shows the $type output for several common types of expressions:

Example                         Results
-------------------             -------------------

{ $type: "a" }                  "string"
{ $type: /a/ }                  "regex"
{ $type: 1 }                    "double"
{ $type: NumberLong(627) }      "long"
{ $type: { x: 1 } }             "object"
{ $type: [ [ 1, 2, 3 ] ] }      "array"

NOTE:
In the case of a literal array such as [ 1, 2, 3 ], 
enclose the expression in an outer set of array brackets to prevent MongoDB from parsing [ 1, 2, 3 ] 
as an argument list with three arguments (1, 2, 3). 
Wrapping the array [ 1, 2, 3 ] in a $literal expression achieves the same result.

See operator expression syntax forms for more information.


Available Types
-------------------

The following table lists the BSON types and the corresponding integer values returned by $type:

Type            Number          Alias                   Notes
-------------------------------------------------------------

Double          1               "double"
String          2               "string"
Object          3               "object"
Array           4               "array"
Binary data     5               "binData"
Undefined       6               "undefined"             Deprecated.
ObjectId        7               "objectId"
Boolean         8               "bool"
Date            9               "date"
Null            10              "null"
Regular 
Expression      11              "regex"
DBPointer       12              "dbPointer"             Deprecated.
JavaScript      13              "javascript"
Symbol          14              "symbol"                Deprecated.
JavaScript
code with 
scope           15              "javascriptWithScope"   Deprecated in MongoDB 4.4.
32-bit integer  16              "int"
Timestamp       17              "timestamp"
64-bit integer  18              "long"
Decimal128      19              "decimal"               
Min key         -1              "minKey"
Max key         127             "maxKey"

If the argument is a field that is missing in the input document, 
$type returns the string "missing".


"""

from typing import Any
from monggregate.base import BaseModel

class Type_(BaseModel):
    """
    Creates a $type expression

    Attributes
    -------------------
        - expression, Any : expression whose type must be evaluated

    """

    expression:Any

    @property
    def statement(self)->dict:

        return self.resolve({
            "$type":self.expression
        })
    

def type_(expression:Any)->Type_:
    """Returns a $type operator"""

    return Type_(
        expression=expression
    )
