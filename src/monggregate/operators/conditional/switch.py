"""
Module defining an interface to the $switch operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/switch/#mongodb-expression-exp.-switch

Definition
-------------------
$switch
Evaluates a series of case expressions. 
When it finds an expression which evaluates to true, 
$switch executes a specified expression and breaks out of the control flow.

The $switch expression has the following syntax:

    >>> {
            $switch: {
                branches: [
                    { case: <expression>, then: <expression> },
                    { case: <expression>, then: <expression> },
                    ...
                ],
                default: <expression>
            }
        }


The objects in the branches array must contain only a case field and a then field.


Behavior
-------------------
The various case statements do not need to be mutually exclusive. 
$switch executes the first branch it finds which evaluates to true. If none of the branches evaluates to true, 
$switch executes the default option.

The following conditions cause $switch to fail with an error:

    * The branches field is missing or is not an array with at least one entry.

    * An object in the branches array does not contain a case field.

    * An object in the branches array does not contain a then field.

    * An object in the branches array contains a field other than case or then.

    * No default is specified and no case evaluates to true.


"""

from typing import Any
from monggregate.operators.conditional.conditional import ConditionalOperator

# TODO : Define branch <VM, 14/08/2023>
# {"case": <expression>, "then": <expression> }

class Switch(ConditionalOperator):
    """
    Creates a $switch expression

    Attributes
    -------------------
        - branches, list[Any] : An array of control branch documents
                                The branches array must contain at least one branch document.
        - default, Any|None : The path to take if no branch case expression evaluates to true.
                         Although optional, if default is unspecified and no branch case evaluates to true, 
                         $switch returns an error.
            
    
    """


    branches : list[Any]
    default : Any|None

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$switch" : {
                "branches" : self.branches,
                "default" : self.default
            }
        })
    
def switch(branches:list[Any], default:Any)->Switch:
    """Returns an $switch operator"""

    return Switch(
        branches=branches,
        default=default
    )