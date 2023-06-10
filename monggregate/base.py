"""Module defining the base class of the package"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod
from typing import Any

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel as PydanticBaseModel, BaseConfig
from humps import camelize

class BaseModel(PydanticBaseModel, ABC):
    """Mongreggate base class"""

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
        alias_generator = camelize


def isbasemodel(instance:Any)->bool:
    """Returns true if instance is an instance of BaseModel"""

    return isinstance(instance, BaseModel)

def resolve(obj:Any)->dict|list[dict]:
        """Resolves an expression encapsulated in an object from a class inheriting from BaseModel"""

        if isbasemodel(obj):
            output:dict|list = obj.statement
        elif isinstance(obj, list) and any(map(isbasemodel, obj)):
            output = []
            for element in obj:
                if isinstance(element, BaseModel):
                    output.append(element.statement)
                else:
                    output.append(element)
        #elif isinstance(expression, dict): # Does this case really exist ?
        else:
            output = obj

        return output
