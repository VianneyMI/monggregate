
"""
Module definining an interface to MongoDB $skip stage operation in aggrgation pipeline.

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 21/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/skip/#mongodb-pipeline-pipe.-skip

# Definition
# ---------------------------------------

Skips over the specified number of documents that pass into the stage and passes the remaining documents to the next stage in the pipeline.

The $skip stage has the following prototype form:

    >>> { $skip: <positive 64-bit integer> }

$skip takes a positive integer that specifies the maximum number of documents to skip.

NOTE : Starting in MongoDB 5.0, the $skip pipeline aggregation has a 64-bit integer limit.
       Values passed to the pipeline which exceed this limit will return an invalid argument error.


# Behavior
#-----------------------------------------

Using $skip with Sorted Results

If using the $skipstage with any of:

    * the $sort aggregation stage,

    * the sort() method, or

    * the sort field to the findAndModify command or the findAndModify() shell method,

be sure to include at least one field in your sort that contains unique values, before passing results to the $skip stage.

Sorting on fields that contain duplicate values may return a different sort order for those duplicate fields over multiple executions,
especially when the collection is actively receiving writes.

The easiest way to guarantee sort consistency is to include the _id field in your sort query.

See the following for more information on each:

    * Consistent sorting with $sort (aggregation)
    (https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#std-label-sort-aggregation-consistent-sorting)

    * Consistent sorting with the sort() shell method
    (https://www.mongodb.com/docs/manual/reference/method/cursor.sort/#std-label-sort-cursor-consistent-sorting)

    * Consistent sorting with the findAndModify command
    (https://www.mongodb.com/docs/manual/reference/command/findAndModify/#std-label-findandmodify-command-consistent-sorting)

    * Consistent sorting with the findAndModify() shell method
    (https://www.mongodb.com/docs/manual/reference/method/db.collection.findAndModify/#std-label-findandmodify-method-consistent-sorting)



"""

#from pydantic import pyd.Field
from monggregate.stages.stage import Stage

class Skip(Stage):
    """
    Creates a skip statement for an aggregation pipeline skip stage.

    Attributes:
    -----------------------
        - statement, dict : the statement generated after instantiation
        - value, int : positive integer representing the number of documents to be skipped.

    """

    value : int # Add gt 0 constraint ? check behavior with 0

    @property
    def statement(self)->dict:
        """Generate statement from arguments"""

        return self.resolve({
            "$skip" : self.value
        })
