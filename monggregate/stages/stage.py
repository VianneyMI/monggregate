"""Stage Module"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel, BaseConfig

# Package imports
# ---------------------------


# NOTE : Stage should be an abstract base class and all operators should be classes inheriting from the base class
class Stage(BaseModel, ABC):
    """MongoDB pipeline stage interface bas class"""

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
