"""
Module definining an interface to MongoDB $group stage operation in aggrgation pipeline

"""

from pydantic import root_validator, Field
from app.stages.stage import Stage

class Group(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    by : str | list[str] | set[str] = Field(..., alias = "_id")
    #operation : Operator # TODO  : After dealing with operators ($sum, $avg, $count, etc...)
    #result : Any
    query : dict



    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        # Retrieving the values
        #---------------------------------------
        by = values.get("by")
        _id = values.get("_id")
        query = values.get("query")

        # Handling aliases
        #---------------------------------------
        if not (_id or by or (query and query.get("_id"))):
            raise TypeError("by (_id) is required")

        if not query:
            raise TypeError("query is required")

        if not _id in query:
            query.update({"_id":_id})

        values["statement"] = query

        return values
