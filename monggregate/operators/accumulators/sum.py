"""
Module defining an interface to MongoDB $sum accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 13/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sum/#mongodb-group-grp.-sum

Definition
-----------------------------

Changed in version 5.0.

Calculates and returns the collective sum of numeric values.
$sum ignores non-numeric values.

    * $sum is available in these stages:
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

In MongoDB 3.2 and earlier, $sum is available in the $group stage only.

Syntax
----------------------

When used in the $bucket, $bucketAuto, $group, and $setWindowFields stages,
$sum has this syntax:
    >>> { $sum: <expression> }

When used in other supported stages,
$sum has one of two syntaxes:

    * $sum has one specified expression as its operand:

    >>> { $sum: <expression> }

    * $sum has a list of specified expressions as its operand:

    >>> { $sum: [ <expression1>, <expression2> ... ]  }

For more information on expressions, see Expressions.

Behavior
------------------------------
Result Data Type

The result will have the same type as the input except when it cannot be represented accurately in that type. In these cases:

    * A 32-bit integer will be converted to a 64-bit integer if the result is representable as a 64-bit integer.

    * A 32-bit integer will be converted to a double if the result is not representable as a 64-bit integer.

    * A 64-bit integer will be converted to double if the result is not representable as a 64-bit integer.

Non-Numeric or Non-Existent Fields

If used on a field that contains both numeric and non-numeric values,
$sum ignores the non-numeric values and returns the sum of the numeric values.

If used on a field that does not exist in any document in the collection,
$sum returns 0 for that field.

If all operands are non-numeric, $sum returns 0.

Array Operand

In the $group stage, if the expression resolves to an array,
$sum treats the operand as a non-numerical value.

In the other supported stages:

    * With a single expression as its operand, if the expression resolves to an array, $sum
      traverses into the array to operate on the numerical elements of the array to return a single value.

    * With a list of expressions as its operand, if any of the expressions resolves to an array,
      $sum does not traverse into the array but instead treats the array as a non-numerical value.

"""

from typing import Any
from monggregate.operators.accumulators.accumulator import Accumulator

class Sum(Accumulator):
    """
    Creates a $sum expression.

    Attributes
    -----------------------
        - operands, list[Expression] : Any valid list of expressions
        - operand, Expression : Any valid expression
    """

    expression : Any


    @property
    def statement(self) -> dict:

        return self.resolve({
            "$sum" : self.expression
        })

def sum(*args:Any)->Sum:
    """Returns a $sum operator"""

    if len(args)>1:
        output = Sum(expression=list(args))
    else:
        output = Sum(expression=args[0])

    return output
