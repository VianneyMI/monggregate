"""
Module defining an interface to $last operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------

Last Updated (in this package) : 12/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/last-array-element/#mongodb-expression-exp.-last

Definition
--------------------------
$last
New in version 4.4
Returns the last element in an array.

NOTE : Disambiguation
       This page describes the $last array operator.
       For the $last aggregation accumulator,
       see [$last (aggregation accumulator)](https://www.mongodb.com/docs/manual/reference/operator/aggregation/last-array-element/#mongodb-expression-exp.-last)

Syntax
--------------------------
The $last operator has the following syntax:

    >>> { $last: <expression> }

The <expression> can be any valid expression as long as it resolves to an array, null, or missing.
For more information on expressions, see Expressions.

The $last operator is an alias for the following $arrayElemAt expression:

    >>> { $arrayElemAt: [ <array expression>, -1 ] }

Behavior
-----------------------
Valid Operands

Valid operand for $last must resolve to an array, null, or missing

    * If the operand resolves to a non-empty array, $last
      returns the first element in the array:

    * If the operand resolves to an empty array [],
      $last does not return a value.

    * If the operand is null or missing,
      $last returns null.

For example, create a test collection example1 with the following documents:

    >>> db.example1.insertMany([
     { "_id" : 1, "x" : [ 1, 2, 3 ] },      // Non-empty array
     { "_id" : 2, "x" : [ [ ] ] },          // Non-empty array
     { "_id" : 3, "x" : [ null ] },         // Non-empty array
     { "_id" : 4, "x" : [ ] },              // Empty array
     { "_id" : 5, "x" : null },             // Is null
     { "_id" : 6 }                          // Is Missing
])

Then, the following adds a new field firstElem whose value is derived from applying the
$last operator to the x field:

    >>> db.example1.aggregate([
   { $addFields: { firstElem: { $last: "$x" } } }
])

The operator returns the following documents:

    >>> { "_id" : 1, "x" : [ 1, 2, 3 ], "firstElem" : 1 }
{ "_id" : 2, "x" : [ [ ] ], "firstElem" : [ ] }
{ "_id" : 3, "x" : [ null ], "firstElem" : null }
{ "_id" : 4, "x" : [ ] }                          // No output
{ "_id" : 5, "x" : null, "firstElem" : null }
{ "_id" : 6, "firstElem" : null }

Invalid Operands

If the operand does not resolve to an array, null, or missing, the aggregation operation as a whole errors.

For example, create a test collection example2 with the following documents:

    >>> db.example2.insertMany([
   { "_id" : 1, "x" : [ 1, 2, 3 ] },
   { "_id" : 2, "x" : 2 },             // x is not an array/null or missing
])

Then, the following aggregation operation returns an error because of the { "_id" : 2, "x" : 2 } document:

    >>> db.example2.aggregate( { $addFields: { firstElem: { $last: "$x" } } } )

That is, the operation returns the following:

    >>> 2020-01-20T18:31:13.431-05:00 E  QUERY    [js] uncaught exception: Error: command failed: {
   "ok" : 0,
   "errmsg" : "$last's argument must be an array, but is double",
   "code" : 28689,
   "codeName" : "Location28689"
} : aggregate failed :



"""

from typing import Any
from monggregate.operators.array.array import ArrayOnlyOperator

class Last(ArrayOnlyOperator):
    """
    Creates a $last expression

    Attributes
    -----------------------------
        - expression, Expression : Any valid expression

    """

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$last":self.expression
        })

def last(array:Any)->Last:
    """Returns a $last operator"""

    return Last(
        expression = array
    )
