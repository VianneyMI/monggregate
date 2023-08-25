"""
Module defining an interface to the $cond operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 14/08/2023
Source : https://docs.mongodb.com/manual/reference/operator/aggregation/cond/#mongodb-expression-exp.-cond

Definition
-------------------
$cond
Evaluates a boolean expression to return one of the two specified return expressions.

The $cond expression has one of two syntaxes:

    >>> { $cond: { if: <boolean-expression>, then: <true-case>, else: <false-case> } }

    or

    >>> { $cond: [ <boolean-expression>, <true-case>, <false-case> ] }


$cond requires all three arguments (if-then-else) for either syntax.

If the <boolean-expression> evaluates to true, then 
$cond evaluates and returns the value of the <true-case> expression. 
Otherwise, $cond evaluates and returns the value of the <false-case> expression.

The arguments can be any valid expression. 
For more information on expressions, see Expressions.

"""

from typing import Any
from monggregate.base import pyd
from monggregate.operators.conditional.conditional import ConditionalOperator

class Cond(ConditionalOperator):
    """
    Creates a $cond expression

    Attributes
    -------------------
        - if_, Any : the boolean expression to evaluate
        - then_, Any : the expression to evaluate if if_ is true
        - else_, Any : the expression to evaluate if if_ is false

        - expression, Any : the boolean expression to evaluate (alias for if_)
        - true_, Any : the expression to evaluate if expression is true (alias for then_)
        - false_, Any : the expression to evaluate if expression is false (alias for else_)

    if_, then_ and else_ have precedence over expression, true_ and false_
    Thus only the first syntax will be used whatever combination of arguments is provided (as long as it is valid)
            
    
    """

    # Syntax 2
    expression : Any|None
    # NOTE: below trailing underscores and aliases might not be needed as true/false are not protected in python
    # (but True and False are) <VM, 14/08/2023>
    true_ : Any|None = pyd.Field(alias="true") 
    false_ : Any|None = pyd.Field(alias="false")

    # Syntax 1
    if_ : Any = pyd.Field(alias="if")
    then_ : Any = pyd.Field(alias="then")
    else_ : Any = pyd.Field(alias="else")

    @pyd.root_validator(pre=True)
    def _validate_conditional(cls, values:dict)->dict:
        """Checks combination of arguments"""

        if_ = values.get("if_")
        then_ = values.get("then_")
        else_ = values.get("else_")

        expression = values.get("expression")
        true_ = values.get("true_")
        false_ = values.get("false_")

        c1 = if_ is not None and then_ is not None and else_ is not None
        c2 = expression is not None and true_ is not None and false_ is not None

        if not (c1 or c2):
            raise ValueError("Either (if_, then_, else_) or (expression, true_, false_) must be provided")
        
        return values
    
    @pyd.validator("if_")
    def _validate_if(cls, v:Any, values:dict)->Any:
        """Checks if_ is not None"""

        if not v:
            return values.get("expression")
        
        return v
    
    @pyd.validator("then_")
    def _validate_then(cls, v:Any, values:dict)->Any:
        """Checks then_ is not None"""

        if not v:
            return values.get("true_")
        
        return v
    
    @pyd.validator("else_")
    def _validate_else(cls, v:Any, values:dict)->Any:
        """Checks else_ is not None"""

        if not v:
            return values.get("false_")
        
        return v

    
    @property
    def statement(self) -> dict:
        return self.resolve({
            "$cond" : {
                "if" : self.if_,
                "then" : self.then_,
                "else" : self.else_
            }
        })
    
def cond(*args:Any, **kwargs:Any)->Cond:
    """Returns an $cond operator"""

    if_ = args[0] if args else (kwargs.get("if_") or kwargs.get("expression"))
    then_ = args[1] if len(args) > 1 else (kwargs.get("then_") or kwargs.get("true_"))
    else_ = args[2] if len(args) > 2 else (kwargs.get("else_") or kwargs.get("false_"))

    return Cond(
        if_=if_,
        then_=then_,
        else_=else_
    )