"""
Module defining an interface to MongoDB $avg accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 13/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/avg/#mongodb-group-grp.-avg

Definition
-----------------------
Changed in version 5.0.

$avg
Returns the average value of the numeric values.
$avgignores non-numeric values.

    * $avg is available in these stages:
    * $addFields (Available starting in MongoDB 3.4)
    * $bucket
    * $bucketAuto
    * $group
    * $match stage that includes an $expr expression
    * $project
    * $replaceRoot (Available starting in MongoDB 3.4)
    * $replaceWith (Available starting in MongoDB 4.2)
    * $set (Available starting in MongoDB 4.2)
    * $setWindowFields (Available starting in MongoDB 5.0)

In MongoDB 3.2 and earlier, $avg is available in the $group stage only.

Syntax
-----------------------

When used in the $bucket, $bucketAuto, $group and $setWindowFields stages, $avg has this syntax:

    >>> { $avg: <expression> }

When used in other supported stages, $avg has one of two syntaxes:

    * $avg has one specified expression as its operand:

    >>> { $avg: <expression> }

    * $avg has a list of specified expressions as its operand:

    >>> { $avg: [ <expression1>, <expression2> ... ]  }

For more information on expressions, see Expressions.

Behavior
-------------------------

Non-numeric or Missing Values

$avg ignores non-numeric values, including missing values. If all of the operands for the average are non-numeric,
$avg returns null since the average of zero values is undefined.

Array Operand

In the $group stage, if the expression resolves to an array, $avg treats the operand as a non-numerical value.

In the other supported stages:

    * With a single expression as its operand, if the expression resolves to an array, $avg
      traverses into the array to operate on the numerical elements of the array to return a single value.

    * With a list of expressions as its operand, if any of the expressions resolves to an array, $avg
      does not traverse into the array but instead treats the array as a non-numerical value.

"""


from typing import Any
from monggregate.operators.accumulators.accumulator import Accumulator

class Average(Accumulator):
    """
    Creates a $avg expression.

    Attributes
    ------------------------
        - expression : Any valid expression

    """

    expression : Any

    @property
    def statement(self) -> dict:

        return self.resolve({
            "$avg" : self.expression
        })
    
Avg = Average

def average(expression:Any)->Average:
    """Returns a $avg operator"""

    return Average(expression=expression)

avg = average
