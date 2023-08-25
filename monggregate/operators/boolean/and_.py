"""
Module defining an interface to the $and operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 19/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/and/#mongodb-expression-exp.-and

Definition
-------------------
$and
Evaluates one or more expressions and returns true if all of the expressions are true or if run with no argument expressions.
Otherwise, $and returns false.

$and syntax:
    >>> { $and: [ <expression1>, <expression2>, ... ] }

For more information on expressions, see Expressions.

Behavior
---------------------

In addition to the false boolean value,
$and evaluates as false the following: null, 0, and undefined values.
The $and evaluates all other values as true, including non-zero numeric values and arrays.

Error Handling
--------------------
To allow the query engine to optimize queries, $and handles errors as follows:

    * If any expression supplied to $and would cause an error when evaluated alone, the $and containing the expression may cause an error but an error is not guaranteed.

    * An expression supplied after the first expression supplied to $and may cause an error even if the first expression evaluates to false.

For example, the following query always produces an error if $x is 0

    >>> db.example.find({
        $expr: { $eq: [ { $divide: [ 1, "$x" ] }, 3 ] }
    })

The following query, which contains multiple expressions supplied to $and, may produce an error if there is any document where $x is 0:

    >>> db.example.find({
        $and: [
            { x: { $ne: 0 } },
            { $expr: { $eq: [ { $divide: [ 1, "$x" ] }, 3 ] } }
        ]
    })

"""

from typing import Any
from monggregate.operators.boolean.boolean import BooleanOperator

class And(BooleanOperator):
    """
    Creates a $and expression

    Attributes
    -------------------
        - expressions, list[Expression] : list of valid expressions,
                                          that serve as operands for the and
                                          operation

    """

    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$and" : self.expressions
        })

def and_(*args:Any)->And:
    """Returns a $and operator"""

    return And(
        expressions=list(args)
    )

