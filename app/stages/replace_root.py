"""
Module definining an interface to MongoDB $replaceRoot stage operation in aggrgation pipeline

"""

from pydantic import root_validator
from app.stages.stage import Stage


class ReplaceRoot(Stage):
    """
    TBD

    """

    statement: dict
    path_to_new_root : str

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict:
        """Generate statements from argument"""

        path_to_new_root:str|None = values.get("path_to_new_root")
        if not path_to_new_root:
            raise TypeError("path_to_new_root is required")

        if not path_to_new_root.startswith("$"):
            path_to_new_root = "$" + path_to_new_root


        values["statement"] = {"$replaceRoot":{"newRoot":path_to_new_root}}

        return values
