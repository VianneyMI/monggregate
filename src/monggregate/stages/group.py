"""
Module defining an interface to MongoDB `$group` stage operation in aggregation pipeline.
"""


from typing import Any
from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.utils import validate_field_path, validate_field_paths

class Group(Stage):
    """
    Abstraction of MongoDB `$group` statement which separates documents 
    into groups according to a "group key".

    Parameters
    ----------
    by :  str | list[str] | set[str] | dict | None
        Field or group of fields to group by
    query : dict | None
        Computed aggregated values (per group)
    
    Online MongoDB documentation:
    -----------------------------
    The `$group` stage separates documents into groups according to a 
    "group key". The output is one document for each unique group key.

    A group key is often a field, or group of fields. The group key can 
    also be the result of an expression. Use the `_id` field in the `$group` 
    pipeline stage to set the group key. See below for usage examples.

    In the `$group` stage output, the `_id` field is set to the group key 
    for that document.

    The output documents can also contain additional fields that are set using
    accumulator expressions.

    NOTE : The group stage does not order its output documents.

    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/)
    """

    by : Any  = pyd.Field(None, alias = "_id") # | or any constant value, in this case
                                                # the stage returns a single document that aggregates values across all of the input documents
    query : dict = {}

    # Validators
    # ------------------------------------------
    _validate_by = pyd.validator("by", pre=True, always=True, allow_reuse=True)(validate_field_path) # re-used pyd.validator
    _validate_iterable_by = pyd.validator("by", pre=True, always=True, allow_reuse=True)(validate_field_paths) # re-used pyd.validator

    @pyd.validator("query", always=True)
    @classmethod
    def validate_query(cls, query:dict, values:dict[str,Any]) -> dict:
        """Validates the query argument"""

        by = values.get("by") # maybe need to check that by is not empty list or empty set

        # maybe need to check query before
        if not "_id" in query:
            query.update({"_id":by})

        return query

    @property
    def statement(self) -> dict[str, dict]:
        """Generates set stage statement from arguments"""


        return  self.resolve({
            "$group":self.query
        })
