"""Operator Module"""

# Standard Library imports
#----------------------------
from abc import ABC, abstractmethod

# 3rd Party imports
# ---------------------------
from pydantic import BaseModel, BaseConfig

# Package imports
# ---------------------------
from monggregate.utils import StrEnum

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

class OperatorEnum(StrEnum):
    """Enumeration of available operators"""

    # TODO : Complete this enum <VM, 30/09/2022>
    ABS = "$abs"
    ACCUMULATOR = "$accumulator"
    ACOS = "$acos"
    ACOSH = "$acosh"
    ADD = "$add"
    ADD_TO_SET = "$addToSet"
    ALL_ELEMENTS_TRUE = "AllElementsTrue"
    AND = "$and"
    ANY_ELEMENTS_TRUE = "$anyElementsTrue"
    ARRAY_ELEM_AT = "$arrayElemAt"
    ARRAY_TO_OBJECT = "$arrayToObject"
    ASIN = "$asin"
    ASINH = "$asinh"
    ATAN = "$atan"
    ATAN2 = "$atan2"
    ATANH = "$atanh2"
    AVG = "$avg"
    BINARY_SIZE = "$binarySize"


