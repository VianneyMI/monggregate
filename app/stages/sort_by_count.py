"""
Module definining an interface to MongoDB $count stage operation in aggrgation pipeline

"""

from pydantic import root_validator
from app.stages.stage import Stage

class SortByCount(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    by : str # TODO : Allow more types <VM, 17/09/2022>


    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        # Retrieving the values
        #---------------------------------------
        by = values.get("by")
        if not by:
            raise TypeError("by is required")

        values["statement"] = {
            "$sortByCount" : by
        }

        return values