"""
Module definining an interface to MongoDB $skip stage operation in aggregation pipelines.

Online MongoDB documentation:
----------------------------------------------------------------------
Last Updated in this package : 24/04/2023
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/unset/#definition

# Definition
# ------------------------
New in version 4.2

Removes/excludes fields from documents.

# Syntax
# ------------------------

The $unset stage has the following syntax:

    * To remove a single field, the $unset takes a string that specifies the field to remove:

        >>> { $unset: "<field>" }

    * To remove multiple fields, the $unset takes an array of fields to remove.

        >>> { $unset: [ "<field1>", "<field2>", ... ] }

# Considerations
# -------------------------------

$unset and $project 

The $unset is an alias for the $project stage that removes/excludes fields:

    >>> { $project: { "<field1>": 0, "<field2>": 0, ... } }

Embedded fields

To remove/exclude a field or fields within an embedded document, you can use the dot notation, as in:

    >>> { $unset: "<field.nestedfield>" }

or

    >>> { $unset: [ "<field1.nestedfield>", ...] }


"""

from monggregate.stages.stage import Stage
from monggregate.fields import FieldName

class Unset(Stage):
    """
    Creates an $unset statement for an aggregation pipeline unset stage.

    Attributes:
    --------------------

        - field, str|None: field to be removed
        - fields, list[str]|None, list of fields to be removed
    
    """

    field : FieldName|None
    fields : list[FieldName]|None

    @property
    def statement(self) -> dict:
        
        if self.field:
            _statement = {
                "$unset":self.field
            }
        else:
            _statement = {
                "$unset":self.fields
            }

        return self.resolve(_statement)
    