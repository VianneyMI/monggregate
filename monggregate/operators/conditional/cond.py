"""
Module defining an interface to $cond operator

"""

from typing import Any
from monggregate.base import pyd
from monggregate.operators.conditional.conditional import ConditionalOperator

class Cond(ConditionalOperator):
    """
    xxx
            
    
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
    """Returns an $cond statement"""

    if_ = args[0] if args else (kwargs.get("if_") or kwargs.get("expression"))
    then_ = args[1] if len(args) > 1 else (kwargs.get("then_") or kwargs.get("true_"))
    else_ = args[2] if len(args) > 2 else (kwargs.get("else_") or kwargs.get("false_"))

    return Cond(
        if_=if_,
        then_=then_,
        else_=else_
    )