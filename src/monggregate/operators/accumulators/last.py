"""
Module defining an interface to MongoDB $last accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 13/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/last/#mongodb-group-grp.-last

Definition
----------------------------

$last
Changed in version 5.0.

Returns the value that results from applying an expression to the last document in a group of documents. Only meaningful when documents are in a defined order.

$last is available in these stages:

    * $bucket
    * $bucketAuto
    * $group
    * $setWindowFields (Available starting in MongoDB 5.0)

NOTE: Disambiguation
This page describes the $last aggregation accumulator.
For the $last array operator, see $last (array operator)

Syntax
----------------------
$last syntax:

    >>> { $last: <expression> }

For more information on expressions, see Expressions.

Behavior
------------------------

To define the document order for $last with the:

    * $group stage, add a $sort stage before the $group stage.
    * $setWindowFields stage, set the sortBy field.

NOTE :
Although the $sort stage passes ordered documents as input to the $group and $setWindowFields stages,
those stages are not guaranteed to maintain the sort order in their own output.

When used with $setWindowFields, $last returns null for empty windows.
An example empty window is a { documents: [ -1, -1 ] } documents window on the last document of a partition.

"""


from typing import Any
from monggregate.operators.accumulators.accumulator import Accumulator

class Last(Accumulator):
    """
    Creates a $last expression.

    Attributes
    ------------------------
        - expression, Expression : Any valid expression

    """

    expression : Any



    @property
    def statement(self) -> dict:

        return self.resolve({
            "$last" : self.expression
        })

def last(expression:Any)->Last:
    """Returns a $last operator"""

    return Last(expression=expression)
