"""Module defining the base class of the package"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel as PydanticBaseModel, BaseConfig

class BaseModel(PydanticBaseModel, ABC):
    """MongoDB pipeline stage interface bas class"""

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