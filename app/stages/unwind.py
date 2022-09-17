"""
Module definining an interface to MongoDB $unwind stage operation in aggrgation pipeline

"""

from pydantic import root_validator, Field
from app.stages.stage import Stage

class Unwind(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    path_to_array : str = Field(..., alias = "path")
    include_array_index : str | None #The name of a new field to hold the array index of the element.
                                        # The name cannot start with a dollar sign $
    always: bool = Field(False, alias="preserve_null_and_empty_arrays")

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        # Retrieving the values passed
        #-------------------------------------------------
        path_to_array:str|None = values.get("path_to_array")
        path:str|None = values.get("path")

        include_array_index:str|None = values.get("include_array_index")
        # NOTE : In the root_validator ahs not set the default value yet when no value is provided for an argument
        # with a default value
        preserve_null_and_empty_arrays:bool|None = values.get("preserve_null_and_empty_arrays")
        always:bool|None = values.get("always")


        # Handling aliases
        #--------------------------------------------------
        if not(path_to_array or path):
            raise TypeError("path_to_array (path) is required")
        elif not path:
            path = path_to_array

        if not(always or preserve_null_and_empty_arrays):
            raise TypeError("always (preserve_null_and_empty_arrays) is required")
        elif not preserve_null_and_empty_arrays:
            preserve_null_and_empty_arrays = always


        # Validates path
        #------------------------------------------
        if not path.startswith("$"):
            path = "$" + path


        # Generate statement
        # -------------------------------------------------
        values["statement"] = {
            "$unwind" : {
                "path":path,
                "includeArrayIndex":include_array_index,
                "preserveNullAndEmptyArrays":preserve_null_and_empty_arrays
            }
        }


        return values
