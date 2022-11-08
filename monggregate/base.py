"""Module defining the base class of the package"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod
from typing import Any

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel as PydanticBaseModel, BaseConfig, validator

class BaseModel(PydanticBaseModel, ABC):
    """Mongreggate base class"""

    @validator("*", pre=True)
    @classmethod
    def resolve(cls, expression:Any)->dict|list[dict]:
        """Resolves an expression encapsulated in an object from a class inheriting from BaseModel"""

        if isinstance(expression, BaseModel):
            output:dict|list = expression.statement
        elif isinstance(expression, list):
            for element in expression:
                output = []
                if isinstance(element, BaseModel):
                    output.append(element.statement)
                else:
                    output.append(element)
        #elif isinstance(expression, dict): # Does this case really exist ?
        else:
            output = expression

        return output

    @property
    @abstractmethod
    def statement(self)->dict:
        """stage stament"""

        # this is a lazy attribute
        # what is currently in generate statement should go in here
        # TODO : Implement cache

    def __call__(self)->dict:
        """Makes an instance of any class inheriting from this class callable"""

        return self.statement

    class Config(BaseConfig):
        """Configuration for Stage classes"""

        allow_population_by_field_name = True
        underscore_attrs_are_private = True
