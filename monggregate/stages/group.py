"""
Module definining an interface to MongoDB $group stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 18/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group

# Definition
---------------------------------

The $group stage separates documents into groups according to a "group key". The output is one document for each unique group key.

A group key is often a field, or group of fields. The group key can also be the result of an expression. Use the _id field in the $group pipeline stage to set the group key. See below for
usage examples.

In the $group stage output, the _id field is set to the group key for that document.

The output documents can also contain additional fields that are set using
accumulator expressions.

NOTE : The group stage does not order its output documents.

The $group stage has the following prototype form:

    >>> {
            $group:{
                    _id: <expression>, // Group key
                    <field1>: { <accumulator1> : <expression1> },
                    ...
            }
        }

The _id and the accumulator operators can accept any valid expression. For more information on expressions, see Expressions.

Considerations
------------------------------
The $group stage has a limit of 100 megabytes of RAM. By default, if the stage exceeds this limit,
$group returns an error. To allow more space for stage processing, use the allowDiskUse option to enable aggregation pipeline stages to write data to temporary files.

Performance Optimizations
------------------------------

This section describes optimizations to improve the performance of
$group. There are optimizations that you can make manually and optimizations MongoDB makes internally.

Optimization to Return the First Document of Each Group

If a pipeline sorts and groups by the same field and the
$group stage only uses the $first accumulator operator, consider adding an index on the grouped field which matches the sort order. In some cases, the
$group stage can use the index to quickly find the first document of each group.

Slot-Based Query Execution Engine
Starting in version 5.2, MongoDB uses the slot-based execution query engine to execute
$group stages if either:

    * $group is the first stage in the pipeline.

    * All preceding stages in the pipeline can also be executed by the slot-based engine.

For more information, see $group Optimization.


"""
from typing import Any
from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.utils import validate_field_path, validate_field_paths

class Group(Stage):
    """
    Creates a group statement for an aggregation pipeline group stage.

    Attributes:
    ------------------------
        - by,  str | list[str] | set[str] | dict | None : field or group of fields to group by
        - query, dict | None : Computed aggregated values (per group)


    """

    by : Any  = pyd.Field(None, alias = "_id") # | or any constant value, in this case
                                                # the stage returns a single document that aggregates values across all of the input documents
    #sum
    #avg
    #count
    #result : Any
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
