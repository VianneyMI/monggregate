"""Operator Module"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel, BaseConfig

# Package imports
# ---------------------------


# NOTE : This is the same interface thant the stage class
# => Need a common ancestor
class Operator(BaseModel, ABC):
    """MongoDB operator abstract base class"""

    _statement : dict = {}# TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]

    @property
    @abstractmethod
    def statement(self)->dict:
        """stage stament"""

        # this is a lazy attribute
        # what is currently in generate statement should go in here
        # TODO : Implement cache

    class Config(BaseConfig):
        """Configuration for Stage classes"""

        allow_population_by_field_name = True
        underscore_attrs_are_private = True

    def __call__(self)->dict:
        """Makes an instance of stage callable"""

        return self.statement
