"""Stage Module"""

from pydantic import BaseModel, BaseConfig

# NOTE : Stage should be an abstract base class and all operators should be classes inheriting from the base class
class Stage(BaseModel):
    """MongoDB pipeline stage interface bas class"""

    statement : dict

    class Config(BaseConfig):
        """Configuration for Stage classes"""

        allow_population_by_field_name = True
