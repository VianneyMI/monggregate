"""
Module definining an interface to MongoDB $limit stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 20/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sample/#mongodb-pipeline-pipe.-sample

Definition
---------------------------

Randomly selects the specified number of documents from the input documents.

The $sample stage has the following syntax:

    >>> { $sample: { size: <positive integer N> } }

N is the number of documents to randomly select.


Behavior
---------------------------
If all of the following conditions are true, $sample uses a pseudo-random cursor to select the N documents:

    * $sample is the first stage of the pipeline.

    * N is less than 5% of the total documents in the collection.

    * The collection contains more than 100 documents.

If any of the previous conditions are false, $sample:

    * Reads all documents that are output from a preceding aggregation stage or a collection scan.

    * Performs a random sort to select N documents.

# NOTE : Random sorts are subject to the sort memory restrictions
(https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#std-label-sort-memory-limit)

#WARNING : MMAPv1 May Return Duplicate Documents
If you are using the:

    * MMAPv1 storage engine, $sample may return the same document more than once in the result set.

    * WiredTiger or in-memory storage engine, $sample does not return duplicate documents.
      WiredTiger is the default storage engine as of MongoDB 3.2.


"""

from monggregate.base import pyd
from monggregate.stages.stage import Stage

class Sample(Stage):
    """
    Creates a sample statement for an aggregation pipeline sample stage.

    Attributes:
    -----------------------
        - statement, dict : the statement generated after instantiation
        - value, int : positive integer representing the number of documents to be randomly picked. Defaults to 10.

    """


    value : int = pyd.Field(10, gt=0)

    @property
    def statement(self)->dict:
        """Generate statement from arguments"""

        return self.resolve({
            "$sample" : {
                "size" : self.value
            }
        })
