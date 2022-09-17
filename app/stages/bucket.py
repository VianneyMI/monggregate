"""
Module definining an interface to MongoDB $bucket stage operation in aggrgation pipeline

"""
# WARNING : This is raw <VM, 17/09/2022>
# No parsing of arguments
# No validation, no helpers, no intelligence just generating the statement for now

from typing import Any
from pydantic import root_validator, Field
from app.stages.stage import Stage

class Bucket(Stage):
    """
    TBD

    """

    statement: dict
    by : str = Field(...,alias="group_by")
    boundaries : list
    default : Any # TODO : Define more precise type
    output : dict

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict:
        """Generates statement from arguments"""

        by = values.get("by")
        #group_by

        boundaries = values.get("boundaries")
        default = values.get("default")
        output = values.get("output")

        # Handling aliases
        #--------------------------------------

        values["statement"] = {
            "$bucket" : {
                "groupBy" : by,
                "boundaries" :boundaries,
                "default" : default,
                "output" : output
            }
        }

        return values






