"""xxxx"""

from typing import Any
from monggregate.base import BaseModel

class Type_(BaseModel):
    """xxxx"""

    expression:Any

    @property
    def statement(self)->dict:

        return self.resolve({
            "$type":self.expression
        })
    

def type_(expression:Any)->Type_:
    """xxxx"""

    return Type_(
        expression=expression
    )
