"""
Module defining an interface to MongoDB $first accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 13/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/first/#mongodb-group-grp.-first


$first
Changed in version 5.0.

Returns the value that results from applying an expression to the first document in a group of documents. Only meaningful when documents are in a defined order.

$first is available in these stages:

    * $bucket
    * $bucketAuto
    * $group
    * $setWindowFields (Available starting in MongoDB 5.0)

NOTE: Disambiguation
This page describes the $first aggregation accumulator.
For the $first array operator, see $first (array operator)

Syntax
----------------------
$first syntax:

    >>> { $first: <expression> }

For more information on expressions, see Expressions.

Behavior
------------------------

To define the document order for $first with the:

    * $group stage, add a $sort stage before the $group stage.
    * $setWindowFields stage, set the sortBy field.

NOTE :
Although the $sort stage passes ordered documents as input to the $group and $setWindowFields stages,
those stages are not guaranteed to maintain the sort order in their own output.

When used with $setWindowFields, $first returns null for empty windows.
An example empty window is a { documents: [ -1, -1 ] } documents window on the first document of a partition.

Missing Values

The documents in a group may be missing fields or may have fields with missing values.

    * If there are no documents from the prior pipeline stage, the $group stage returns nothing.

    * If the field that the $first accumulator is processing is missing, $first returns null.

See the missing data example.

"""


from typing import Any
from monggregate.operators.accumulators.accumulator import Accumulator

class First(Accumulator):
    """
    Creates a $first expression.

    Attributes
    ------------------------
        - expression, Expression : Any valid expression
    """

    expression : Any


    @property
    def statement(self) -> dict:

        return self.resolve({
            "$first" : self.expression
        })

def first(expression:Any)->First:
    """Returns a $first operator"""

    return First(expression=expression)
