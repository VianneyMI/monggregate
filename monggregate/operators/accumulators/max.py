"""
Module defining an interface to MongoDB $max accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 13/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/max/#mongodb-group-grp.-max


Definition
-----------------------------
Changed in version 5.0.

$max
Returns the maximum value.
$max compares both value and type, using the specified BSON comparison order for values of different types.

    * $max is available in these stages:
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

In MongoDB 3.2 and earlier, $max is available in the $group stage only.

Syntax
-----------------------------

When used in the $bucket, $bucketAuto, $group, and $setWindowpyd.Fields stages,
$max has this syntax:

    >>> { $max: <expression> }

When used in other supported stages,
$max has one of two syntaxes:

$max has one specified expression as its operand:

    >>> { $max: <expression> }

$max has a list of specified expressions as its operand:

    >>> { $max: [ <expression1>, <expression2> ... ]  }

For more information on expressions, see Expressions.

Behavior
--------------------------------

Null or Missing Values

If some, but not all, documents for the $max operation have either a null value for the field or are missing the field, the
$max operator only considers the non-null and the non-missing values for the field.

If all documents for the $maxoperation have null value for the field or are missing the field, the $max operator returns null for the maximum value.

Array Operand

In the $group and $setWindowpyd.Fields stages, if the expression resolves to an array,
$max does not traverse the array and compares the array as a whole.

In the other supported stages:

With a single expression as its operand, if the expression resolves to an array,
$max traverses into the array to operate on the numerical elements of the array to return a single value.

With a list of expressions as its operand, if any of the expressions resolves to an array,
$max does not traverse into the array but instead treats the array as a non-numerical value.

"""


from typing import Any
from monggregate.operators.accumulators.accumulator import Accumulator

class Max(Accumulator):
    """
    Creates a $max expression.

    Attributes
    ---------------------
        - expression, Expression : Any valid expression
    """

    expression : Any



    @property
    def statement(self) -> dict:

        return self.resolve({
            "$max" : self.expression
        })

def max(expression:Any)->Max:
    """Returns a $last operator"""

    return Max(expression=expression)
