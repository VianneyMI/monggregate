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

from pydantic import root_validator, Field
from monggregate.stages.stage import Stage
from monggregate.utils import to_unique_list

class Group(Stage):
    """
    Creates a group statement for an aggregation pipeline group stage.

    Attributes:
    ------------------------
        - by / _id (offcial MongoDB name represented by a pydantic alias), str | list[str] | set[str] : field or group of fields to group on
        - query, dict | None : Computed aggregated values (per group)


    """

    by : str | list[str] | set[str] = Field(..., alias = "_id")
    #operation : Operator # TODO  : After dealing with operators ($sum, $avg, $count, etc...)
    #result : Any
    query : dict = {}



    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        # Retrieving the values
        #---------------------------------------
        by = values.get("by")
        _id = values.get("_id")
        query = values.get("query", {})

        # Handling aliases
        #---------------------------------------
        if not (_id or by or (query and query.get("_id"))):
            raise TypeError("by (_id) is required")

        if not _id:
            _id = by

        # Validates query
        #---------------------------------------
        _id = to_unique_list(_id)

        if not query:
            query = {}

        # Generate statement
        #--------------------------------------
        if not "_id" in query:
            query.update({"_id":_id})

        values["statement"] = {
            "$group":query
        }

        return values