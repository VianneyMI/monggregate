"""
Module defining an interface to the $ifNull operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/ifNull/#mongodb-expression-exp.-ifNull

Definition
-------------------
$ifNull
Changed in version 5.0.

The $ifNull expression evaluates input expressions for null values and returns:

    * The first non-null input expression value found.

    * A replacement expression value if all input expressions evaluate to null.

$ifNull treats undefined values and missing fields as null.

Syntax:

    >>> {
            $ifNull: [
                <input-expression-1>,
                ...
                <input-expression-n>,
                <replacement-expression-if-null>
            ]
        }

In MongoDB 4.4 and earlier versions, $ifNull only accepts a single input expression:
$ifNull requires all three arguments (if-then-else) for either syntax.

    >>> {
            $ifNull: [
                <input-expression>,
                <replacement-expression-if-null>
            ]
        }


"""

from typing import Any
from monggregate.operators.conditional.conditional import ConditionalOperator

class IfNull(ConditionalOperator):
    """
    Creates a $cond expression

    Attributes
    -------------------
        - expression, Any : the boolean expression to evaluate
        - output, Any : the expression to evaluate if expression is null
            
    
    """


    expression : Any # NOTE : Maybe diverge from Mongo and do not allow multiple expressions <VM, 14/08/2023>
    output : Any

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$ifNull" : [self.expression, self.output]
        })
    
def if_null(expression:Any, output:Any)->IfNull:
    """Returns an $if_null operator"""

    return IfNull(
        expression=expression,
        output=output
    )
