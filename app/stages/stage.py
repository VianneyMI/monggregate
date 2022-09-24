"""Stage Module"""

from pydantic import BaseModel, BaseConfig

# NOTE : Stage should be an abstract base class and all operators should be classes inheriting from the base class
class Stage(BaseModel):
    """MongoDB pipeline stage interface bas class"""

    _statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]

    class Config(BaseConfig):
        """Configuration for Stage classes"""

        allow_population_by_field_name = True


    def __call__(self)->dict:
        """Makes an instance of stage callable"""

        return self._statement
