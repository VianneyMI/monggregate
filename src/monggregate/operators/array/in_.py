"""
Module defining an interface to $in operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------

Last Updated (in this package) : 12/11/2022
Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/in/#mongodb-expression-exp.-in

Definition
----------------------

$in
Returns a boolean indicating whether a specified value is in an array.
NOTE : This document describes the $in aggregation operator. For the $in query operator see [$in](mongodb.com/docs/manual/reference/operator/query/in/)

$in has the following operator expression syntax:
    >>> { $in: [ <expression>, <array expression> ] }

        Operand             Description
    *  <expression>         Any valid expression.
    *  <array expression>   Any valid expression that resolves to an array.

WARNING : Unlike the $in query operator, the aggregation $in operator does not support matching by regular expressions.

Behavior
-----------------------
$in fails with an error in either of the following cases: if the $in expressions is not given exactly two arguments,
or if the second argument does not resolve to an array.

"""

from typing import Any
from monggregate.operators.array.array import ArrayOperator

class In(ArrayOperator):
    """
    Creates a $in expression

    Attributes
    ------------------------------
        - left, Expression : Any valid expression (to be looked for in right)
        - right, Expression : Any valid expression that resolves to an array (containing left or not).

    """

    left : Any
    right : Any


    @property
    def statement(self) -> dict:
        return self.resolve({
            "$in":[self.left, self.right]
        })

def in_(left:Any, right:Any)->In:
    """Returns a $maxN operator"""

    return In(
        left = left,
        right = right
    )
