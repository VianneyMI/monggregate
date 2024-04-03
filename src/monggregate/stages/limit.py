"""
Module defining an interface to MongoDB `$limit` stage operation in aggregation pipeline.
"""

from monggregate.base import pyd
from monggregate.stages.stage import Stage

class Limit(Stage):
    """
    Abstraction for MongoDB `$limit` statement that limits the number of 
    documents passed to the next stage in the pipeline.

    Parameters
    ----------
    value, int
        The actual limit to apply. Limits the number of documents returned 
        by the stage to the provided value.

    Online MongoDB documentation:
    -----------------------------
    Limits the number of documents passed to the next stage in the pipeline.
    
    `$limit` takes a positive integer that specifies the maximum number of documents to pass along.

    NOTE : Starting in MongoDB 5.0, the `$limit` pipeline aggregation has a 64-bit integer limit. Values
    passed to the pipeline which exceed this limit will return a invalid argument error.

    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/limit/)
    """
    
    value : int = pyd.Field(gt=0)

    @property
    def statement(self)->dict:

        return self.resolve({
            "$limit" : self.value
        })
