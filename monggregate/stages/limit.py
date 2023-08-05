"""
Module definining an interface to MongoDB $limit stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 18/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group

Limits the number of documents passed to the next stage in the pipeline.

The $limit stage has the following prototype form:

    >>> { $limit: <positive 64-bit integer> }

$limit takes a positive integer that specifies the maximum number of documents to pass along.

NOTE : Starting in MongoDB 5.0, the $limit pipeline aggregation has a 64-bit integer limit. Values
passed to the pipeline which exceed this limit will return a invalid argument error.

Behavior
-----------------------------------

Using $limit with Sorted Results

If using $limit stage with any of:

    * the $sort aggregation stage,
    * the sort() method, or
    * the sort field to the findAndModify command or the
      findAndModify() shell method,

be sure to include at least one field in your sort that contains unique values, before
passing results to the $limit stage.

Sorting on fields that contain duplicate values may return an inconsistent sort order for those duplicate fields over multiple executions,
especially when the collection is actively receiving writes.

The easiest way to guarantee sort consistency is to include the _id field in your sort query.

See the following for more information on each:

    * Consistent sorting with $sort (aggregation) : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#std-label-sort-aggregation-consistent-sorting
    * Consistent sorting with the sort() shell method : https://www.mongodb.com/docs/manual/reference/method/cursor.sort/#std-label-sort-cursor-consistent-sorting
    * Consistent sorting with the findAndModify command : https://www.mongodb.com/docs/manual/reference/command/findAndModify/#std-label-findandmodify-command-consistent-sorting
    * Consistent sorting with the findAndModify() shell method : https://www.mongodb.com/docs/manual/reference/method/db.collection.findAndModify/#std-label-findandmodify-method-consistent-sorting


"""

from monggregate.base import pyd
from monggregate.stages.stage import Stage

class Limit(Stage):
    """
    Creates a $limit statement for an aggregation pipeline $limit stage.

    Attributes:
    ---------------------------------
        - value, int : the actual limit to apply.
                       limits the number of documents returned by the stage to
                       the provided value.

    """

    value : int = pyd.Field(gt=0)

    @property
    def statement(self)->dict:

        return self.resolve({
            "$limit" : self.value
        })
