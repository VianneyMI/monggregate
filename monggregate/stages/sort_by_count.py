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

from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.utils import validate_field_path

class SortByCount(Stage):
    """
    Creates a sort_by_count statement for an aggregation pipeline sort_by_count stage

    Attributes:
    -------------------------
        - _statement, dict : the statement generated during the validation process
        - by, str : the key to group, sort and count on

    """

    by : str # TODO : Allow more types <VM, 17/09/2022>

    # Validators
    # ------------------------
    _validates_path_to_array = pyd.validator("by", allow_reuse=True, pre=True, always=True)(validate_field_path)


    @property
    def statement(self)->dict:
        """Generates sort_by_count stage statement from SortByCount class keywords arguments"""

        return  self.resolve({
            "$sortByCount" : self.by
        })
