"""Stage Module"""

from pydantic import BaseModel

# NOTE : Stage should be an abstract base class and all operators should be classes inheriting from the base class
class Stage(BaseModel):
    """MongoDB pipeline stage interface bas class"""

    statement : dict
