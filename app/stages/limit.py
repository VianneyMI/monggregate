"""
Module definining an interface to MongoDB $limit stage operation in aggrgation pipeline

"""

from pydantic import root_validator
from app.stages.stage import Stage

class Limit(Stage):
    """
    TBD

    """

    statement : dict
    value : int

    @root_validator
    @classmethod
    def generate_statement(cls, values:dict)->dict:
        """Generate statement from arguments"""

        value = values.get("value")

        values["statement"] = {
            "$limit" : value
        }

        return values