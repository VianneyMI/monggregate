"""
Module defining an interface to MongoDB $count accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 13/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/count-accumulator/#mongodb-group-grp.-count


Definition
--------------------------
New in version 5.0.

$count
Returns the number of documents in a group.

$count is available in these stages:

    * $bucket
    * $bucketAuto
    * $group
    * $setWindowpyd.Fields (Available starting in MongoDB 5.0)

NOTE : Disambiguation
This page describes the
$count aggregation accumulator. For the $count aggregation pipeline stage, [see $count (aggregation pipeline)](https://www.mongodb.com/docs/manual/reference/operator/aggregation/count/#mongodb-pipeline-pipe.-count)

$count has the following prototype form:

    >>> { $count: <string> }

<string> is the name of the output field which has the count as its value. <string> must be a non-empty string, must not start with $ and must not contain the . character.

Behavior
------------------------
The $count stage is equivalent to the following $group + $project sequence:

    >>> db.collection.aggregate( [
        { $group: { _id: null, myCount: { $sum: 1 } } },
        { $project: { _id: 0 } }
    ] )

where myCount would be the output field that contains the count. You can specify another name for the output field.

"""


from monggregate.operators.accumulators.accumulator import Accumulator

class Count(Accumulator):
    """
    Creates a $count expression.

    """



    @property
    def statement(self) -> dict:

        return self.resolve({
            "$count" : {}
        })

def count()->Count:
    """Returns a $count operator"""

    return Count()

