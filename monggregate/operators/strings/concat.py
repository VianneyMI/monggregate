"""
Module defining an interface to the $concat operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/concat/#mongodb-expression-exp.-concat

Definition
-------------------
$concat
Concatenates strings and returns the concatenated string.

$concat has the following syntax:
    >>> { $concat: [ <expression1>, <expression2>, ... ] }

The arguments can be any valid expression as long as they resolve to strings. For more information on expressions, see Expressions.

If the argument resolves to a value of null or refers to a field that is missing, 
$concat returns null.

"""

from typing import Any
from monggregate.operators.strings.string import StringOperator

class Concat(StringOperator):
    """
    Creates a $concat expression

    Attributes
    -------------------
        - expressions, list[Any] : the list of expressions that must resolve to strings to be concatenated
            
    
    """


    expressions : list[Any]

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$concat" : self.expressions
        })
    
def concat(*args:Any)->Concat:
    """Returns an $concat operator"""

    return Concat(
        expressions=list(args)
    )