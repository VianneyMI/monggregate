"""Module defining the base class of the package"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod
from typing import Any

# 3rd Party imports
# ---------------------------
import pydantic
if pydantic.__version__.startswith("1"):
    from pydantic import BaseModel as PydanticBaseModel, BaseConfig, ValidationError, Field, validator
else:
    from pydantic.v1 import BaseModel as PydanticBaseModel, BaseConfig, ValidationError, Field, validator
    
from humps import camelize

class BaseModel(PydanticBaseModel, ABC):
    """Mongreggate base class"""

    @classmethod
    def resolve(cls, obj:Any)->dict|list[dict]:
        """Resolves an expression encapsulated in an object from a class inheriting from BaseModel"""

        return resolve(obj)

    @property
    @abstractmethod
    def statement(self)->dict:
        """Stage statement absctract method"""

        # this is a lazy attribute
        # what is currently in generate statement should go in here

    def __call__(self)->dict:
        """Makes an instance of any class inheriting from this class callable"""

        return self.resolve(self.statement)

    class Config(BaseConfig):
        """Base configuration for classes inheriting from this"""

        allow_population_by_field_name = True
        underscore_attrs_are_private = True
        smart_union = True
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
        elif isinstance(obj, dict):
            output = {}
            for key, value in obj.items():
                if isinstance(value, BaseModel):
                    output[key] = value.statement
                else:
                    output[key] = resolve(value)
        else:
            output = obj

        return output
