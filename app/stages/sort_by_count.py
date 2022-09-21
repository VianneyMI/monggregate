"""
Module definining an interface to MongoDB $count stage operation in aggrgation pipeline.

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 21/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sortByCount/#mongodb-pipeline-pipe.-sortByCount

Definition
--------------------------------------
Groups incoming documents based on the value of a specified expression, then computes the count of documents in each distinct group.

Each output document contains two fields: an _id field containing the distinct grouping value,
and a count field containing the number of documents belonging to that grouping or category.

The documents are sorted by count in descending order.

The $sortByCount stage has the following prototype form:

    >>> { $sortByCount:  <expression> }


Considerations
--------------------------------------
$sortByCount is subject to the 100 megabyte memory usage limit, but is able to write temporary files to disk if additional space is required.

Starting in MongoDB 6.0, pipeline stages that require more than 100 megabytes of memory to execute write temporary files to disk by default.
In earlier verisons of MongoDB, you must pass { allowDiskUse: true } to individual find and aggregate commands to enable this behavior.

Individual find and aggregate commands may override the allowDiskUseByDefault parameter by either:

    * Using { allowDiskUse: true } to allow writing temporary files out to disk when allowDiskUseByDefault is set to false

    * Using { allowDiskUse: false } to prohibit writing temporary files out to disk when allowDiskUseByDefault is set to true

See also : [Aggregation Pipeline Limits](https://www.mongodb.com/docs/manual/core/aggregation-pipeline-limits)

Behavior
--------------------------------------
The $sortByCount stage is equivalent to the following
$group + $sort sequence:

    >>> { $group: { _id: <expression>, count: { $sum: 1 } } },
    >>> { $sort: { count: -1 } }


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