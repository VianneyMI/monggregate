"""
Module defining an interface to $mergeObjects operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/mergeObjects/#mongodb-expression-exp.-mergeObjects

Definition
------------------
$mergeObjects
Combines multiple documents into a single document.

$mergeObjects is available in these stages:

    * $bucket
    * $bucketAuto
    * $group

Syntax
------------------
When used as a $bucket, $bucketAuto, or $group stage accumulator,
$mergeObjects has this syntax:

    >>> { $mergeObjects: <document> }
When used in other expressions (including in $bucket, $bucketAuto, and $group stages) but not as an accumulator,
$mergeObjects has this syntax:

    >>> { $mergeObjects: [ <document1>, <document2>, ... ] }

The <document> can be any valid expression that resolves to a document.

Behavior
-------------------
$mergeObjects ignores null operands. If all the operands to $mergeObjects resolves to null,
$mergeObjects returns an empty document { }.

$mergeObjects overwrites the field values as it merges the documents.
If documents to merge include the same field name, the field,
in the resulting document, has the value from the last document merged for the field.

"""

from typing import Any
from monggregate.operators.array.array import ArrayOperator

class MergeObjects(ArrayOperator):
    """
    Creates an $arrayToObject expression

    Attribute
    ---------------------
        - expression, Expression : Any valid expression or list of expression

    """

    expression : Any | list[Any]


    @property
    def statement(self) -> dict:
        return self.resolve({
            "$mergeObjects" : self.expression
        })

def merge_objects(expression:Any)->MergeObjects:
    """Returns a $mergeObjects operator"""

    return MergeObjects(expression=expression)
