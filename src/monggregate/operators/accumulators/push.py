"""
Module defining an interface to MongoDB $push accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 13/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/push/#mongodb-group-grp.-push


Definition
---------------------
$push
$push returns an array of all values that result from applying an expression to documents.

$push is available in these stages:

    * $bucket
    * $bucketAuto
    * $group
    * $setWindowFields (Available starting in MongoDB 5.0)

Syntax
--------------------
$push syntax:
    >>> { $push: <expression> }

For more information on expressions, see Expressions.

"""

from typing import Any
from monggregate.operators.accumulators.accumulator import Accumulator

class Push(Accumulator):
    """
    Creates a $push expression.

    Attributes
    -------------------
        - expression, Expression : Any valid expression

    """

    expression : Any



    @property
    def statement(self) -> dict:

        return self.resolve({
            "$push" : self.expression
        })

def push(expression:Any)->Push:
    """Returns a $push operator"""

    return Push(expression=expression)
