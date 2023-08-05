"""
Module definining an interface to MongoDB $unwind stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 21/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/#mongodb-pipeline-pipe.-unwind


Definition
--------------------------------------------
Deconstructs an array field from the input documents to output a document for each element.
Each output document is the input document with the value of the array field replaced by the element.


Syntax
--------------------------------------------
You can pass a field path operand or a document operand to unwind an array field.

Field Path Operand

You can pass the array field path to $unwind. When using this syntax,
$unwindvdoes not output a document if the field value is null, missing, or an empty array.

    >>> { $unwind: <field path> }

When you specify the field path, prefix the field name with a dollar sign $ and enclose in quotes.

Document Operant with Options

You can pass a document to $unwind to specify various behavior options.
    >>> {
            $unwind:
                {
                path: <field path>,
                includeArrayIndex: <string>,
                preserveNullAndEmptyArrays: <boolean>
                }
        }


Behaviors
--------------------------------------------

Non-Array Field Path

`Changed in version 3.2`
$unwind stage no longer errors on non-array operands. If the operand does not resolve to an array but is not missing, null, or an empty array,
$unwind treats the operand as a single element array. If the operand is null, missing, or an empty array, the behavior of
$unwind depends on the value of the preserveNullAndEmptyArrays option.

Previously, if a value in the field specified by the field path is not an array,

    >>> db.collection.aggregate()

generates an error.

Missing Field

If you specify a path for a field that does not exist in an input document or the field is an empty array,
$unwind, by default, ignores the input document and will not output documents for that input document.

To output documents where the array field is missing, null or an empty array, use the
preserveNullAndEmptyArrays option.

"""

from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.utils import validate_field_path

class Unwind(Stage):
    """
    Creates a unwind statement for an aggregation pipeline unwind stage.

    Attributes:
    ---------------------------------

        - path_to_array (path), str : path to an array field
        - include_array_index, str : name of a new field to hold the array index of the element
                                    NOTE : The name cannot start with a dollar sign
        - always (preserve_null_and_empty_index), bool : whether to output documents for input documents where the path does not resolve to a valid array. Defaults to False

    """

    # Attributes
    # ----------------------
    path_to_array : str = pyd.Field(..., alias = "path")
    include_array_index : str | None = None #The name of a new field to hold the array index of the element.
                                        # The name cannot start with a dollar sign $
    always: bool = pyd.Field(False, alias="preserve_null_and_empty_arrays")

    # Validators
    # ------------------------
    _validates_path_to_array = pyd.validator("path_to_array", allow_reuse=True, pre=True, always=True)(validate_field_path)

    @property
    def statement(self)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        params = {"path":self.path_to_array}

        if self.include_array_index:
            params["includeArrayIndex"] = self.include_array_index

        if self.always:
            params["preserveNullAndEmptyArrays"] = self.always

        return  self.resolve({"$unwind" : params})
