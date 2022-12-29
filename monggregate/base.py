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

        def isbasemodel(instance:Any)->bool:
            """Returns true if instance is an instance of BaseModel"""

            return isinstance(instance, BaseModel)

        if isbasemodel(expression):
            output:dict|list = expression.statement
        elif isinstance(expression, list) and any(map(isbasemodel, expression)):
            output = []
            for element in expression:
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
        """Stage statement absctract method"""

        # this is a lazy attribute
        # what is currently in generate statement should go in here


    def __call__(self)->dict:
        """Makes an instance of any class inheriting from this class callable"""

        return self.statement

    class Config(BaseConfig):
        """Base configuration for classes inheriting from this"""

        allow_population_by_field_name = True
        underscore_attrs_are_private = True
