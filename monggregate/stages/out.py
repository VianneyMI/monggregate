"""
Module definining an interface to MongoDB $count stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 23/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out

Definition
----------------------------------
Takes the documents returned by the aggregation pipeline and writes them to a specified collection. Starting in MongoDB 4.4, you can specify the output database.

The $out stage must be the last stage in the pipeline. The $out operator lets the aggregation framework return result sets of any size.

WARNING : $out replaces the specified collection if it exists.
See [Replace Existing Collection](https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/#std-label-replace-existing-collection) for details.

Syntax
----------------------------------
The $out stage has the following syntax:

    * Starting in MongoDB 4.4, $out can take a document to specify the output database as well as the output collection:
        >>> { $out: { db: "<output-db>", coll: "<output-collection>" } }

    * $out can take a string to specify only the output collection (i.e. output to a collection in the same database):
        >>> { $out: "<output-collection>" } // Output collection is in the same database

IMPORTANT :

    * You cannot specify a sharded collection as the output collection. The input collection for a pipeline can be sharded. To output to a sharded collection, see
      $merge (Available starting in MongoDB 4.2).

    * The $out operator cannot write results to a capped collection.

    * If you modify a collection with an Atlas Search index, you must first delete and then re-create the search index.
      Consider using $merge instead.

Behaviors
--------------------------------------

### $out Read Operations Run on Secondary Replica Set Members

Starting in MongoDB 4.4, $out can run on replica set secondary nodes
if all the nodes in cluster have featureCompatibilityVersion set to 4.4 or higher and the Read Preference is set to secondary.

Read operations of the $out statement occur on the secondary nodes, while the write operations occur only on the primary nodes.

Not all driver versions support targeting of $outoperations to replica set secondary nodes.
Check your driver documentation to see when your driver added support for $out running on a secondary.

### Create New Collection

The $out operation creates a new collection if one does not already exist.

The collection is not visible until the aggregation completes. If the aggregation fails, MongoDB does not create the collection.

### Replace Existing Collection

If the collection specified by the $out operation already exists, then upon completion of the aggregation, the
$out stage atomically replaces the existing collection with the new results collection.
Specifically, the $out operation:

    1. Creates a temp collection.

    2. Copies the indexes from the existing collection to the temp collection.

    3. Inserts the documents into the temp collection.

    4. Calls the renameCollectionbcommand with dropTarget: true to rename the temp collection to the destination collection.

The $out operation does not change any indexes that existed on the previous collection. If the aggregation fails, the
$out operation makes no changes to the pre-existing collection.

### Index Constraints

The pipeline will fail to complete if the documents produced by the pipeline would violate any unique indexes, including the index on the _id field of the original output collection.

If the $out operation modifies a collection with an Atlas Searchbindex, you must delete and re-create the search index.
Consider using $merge instead.

### majority Read Concern

Starting in MongoDB 4.2, you can specify read concern level "majority"bfor an aggregation that includes an $out stage.

In MongoDB 4.0 and earlier, you cannot include the $out stage to use "majority" read concern for the aggregation.

### Interaction with mongodump

A mongodumpstarted with --oplog fails if a client issues an aggregation pipeline that includes $outduring the dump process.
See mongodump --oplog for more information.

Restrictions
-----------------------------------------

    * Transactions : An aggregation pipeline cannot use $out inside transactions.

    * Time Series Collections : An aggregation pipeline cannot use $out to output to a time series collection.

    * View Definition : The $out stage is not allowed as part of a view definition. If the view definition includes nested pipeline (e.g. the view definition includes
                        $lookup or $facet stage), this $out stage restriction applies to the nested pipelines as well.

    * $lookup stage : Starting in 4.2, you cannot include the $out stage in the $lookup stage's nested pipeline.

    * $facet stage : $facets tage's nested pipeline cannot include the $out stage.

    * $unionWith stage : $unionWith stage's nested pipeline cannot include the $out stage.

    * "linearizable" read concern : Starting in MongoDB 4.2, the $out stage cannot be used in conjunction with read concern
                                    "linearizable". That is, if you specify "linearizable" read concern for db.collection.aggregate(),
                                    you cannot include the $outbstage in the pipeline.

"""

from monggregate.base import pyd
from monggregate.stages.stage import Stage

class Out(Stage):
    """
    Creates a out statement for an aggregation pipeline out stage.

    Attributes:
    ---------------------------
        - db, str|None : name of the db to output the collection. Defaults to current collection.
        - collection, str : name of the output collection

    """

    db : str|None
    collection : str = pyd.Field(...,alias="coll")

    @property
    def statement(self)->dict:
        """Generates statement from attributes"""


        # Generate statement
        # -------------------------------
        if self.db:
            statement = {
                "$out" : {
                    "db":self.db,
                    "coll":self.collection
                }
            }
        else:
            statement = {
                "$out" : self.collection
            }

        return self.resolve(statement)
