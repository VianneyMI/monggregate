"""
Module definining an interface to MongoDB $set stage operation in aggrgation pipeline

"""

from pydantic import root_validator
from app.stages.stage import Stage

class Set(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    document : dict ={} #| None

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        document = values.get("document")
        values["statement"] = {"$set":document}

        return values
