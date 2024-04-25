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
from monggregate.base import Expression
from monggregate.operators.accumulators.accumulator import Accumulator

class Push(Accumulator):
    """
    Abstraction of MongoDB $push operator.

    Attributes
    -------------------
        - operand, Any:Any valid expression

    Online MongoDB documentation
    ----------------------------
    $push returns an array of all values that result from applying an expression to documents.

    $push is available in these stages:
        * $bucket
        * $bucketAuto
        * $group
        * $setWindowFields (Available starting in MongoDB 5.0)

    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/push/#mongodb-group-grp.-push)
    """

    operand : Any



    @property
    def expression(self) -> Expression:

        return self.express({
            "$push" : self.operand
        })

def push(operand:Any)->Push:
    """Returns a $push operator"""

    return Push(operand=operand)
