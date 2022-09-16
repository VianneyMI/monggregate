"""Stage Module"""

from typing import Any
from pydantic import BaseModel

class Stage(BaseModel):
    """MongoDB pipeline stage interface"""

    current : dict

    def run(self)-> None:
        """Runs the current stage"""

        raise NotImplementedError

    # NOTE : instead of defining classmethods for each aggregation operator. Stage should be an abstract base class and all operators should be classes inheriting from the base class
    @classmethod
    def match(query:dict|None, **kwargs:Any)->dict:
        """
        Filters the documents to pass only the documents that match the specified condition(s) to the next pipeline stage.

        The  $match stage has the following prototype form:
        >>> { $match: { <query> } }


        """
        raise NotImplementedError
