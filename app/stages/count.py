"""
Module definining an interface to MongoDB $count stage operation in aggrgation pipeline

"""

from pydantic import root_validator, Field
from app.stages.stage import Stage

class Count(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    name : str


    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        # Retrieving the values
        #---------------------------------------
        name = values.get("name")
        if not name:
            raise TypeError("name is required")

        values["statement"] = {
            "$count" : name
        }

        return values