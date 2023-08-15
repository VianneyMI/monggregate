"""
Module defining the base classes of the package.

All the classes of the package inherit from one of the classes defined in this module.
"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod
from typing import Any, TypeGuard

# 3rd Party imports
# ---------------------------
try:
    import pydantic.v1 as pyd
except ModuleNotFoundError:
    import pydantic as pyd

    
from humps.main import camelize

class Singleton:
    """Singleton metaclass"""

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class BaseModel(pyd.BaseModel, ABC):
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

    class Config(pyd.BaseConfig):
        """Base configuration for classes inheriting from this"""

        allow_population_by_field_name = True
        underscore_attrs_are_private = True
        smart_union = True
        alias_generator = camelize


def isbasemodel(instance:Any)->TypeGuard[BaseModel]:
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
