
"""
Module definining an interface to MongoDB $skip stage operation in aggrgation pipeline

"""

from pydantic import root_validator
from app.stages.stage import Stage

class Skip(Stage):
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
            "$skip" : value
        }

        return values