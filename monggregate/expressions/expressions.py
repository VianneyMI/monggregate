"""Expressions Module"""

# https://github.com/pydantic/pydantic/issues/2279
# https://stackoverflow.com/questions/53638973/recursive-type-annotations
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python

# Standard Library imports
#----------------------------
from typing import Any
from monggregate.base import BaseModel
from monggregate.operators.boolean import And, Or, Not
#from numbers import Number
# 3rd Party imports
# ---------------------------

class Expression(BaseModel):

    field : str

    @property
    def statement(self)->Any:
        return self.field


    def __and__(self, other:"Expression")->dict:
        """Python $ (and) operator overload"""

        return And(expressions=[self, other]).statement

if __name__ == "__main__":
    result = Expression(field="left") & Expression(field="right")
    print(result)
