"""
Module defining an interface to $or operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/or/#mongodb-expression-exp.-or

Definition
-----------------
$or
Evaluates one or more expressions and returns true if any of the expressions are true.
Otherwise, $or returns false.

$or has the following syntax:
    >>> { $or: [ <expression1>, <expression2>, ... ] }

For more information on expressions, see Expressions.

Behavior
------------------
In addition to the false boolean value,
$or evaluates as false the following: null, 0, and undefined values. The
$or evaluates all other values as true, including non-zero numeric values and arrays.

"""

from typing import Any
from monggregate.operators.boolean.boolean import BooleanOperator

class Or(BooleanOperator):
    """
    Creates a $or expression

    Attributes
    -------------------
        - expressions, list[Expression] : list of valid expressions,
                                          that serve as operands for the or
                                          operation

    """

    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$or" : self.expressions
        })

def or_(*args:Any)->Or:
    """Returns a $or operator"""

    return Or(
        expressions=list(args)
    )
