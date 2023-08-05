"""
Module defining an interface to MongoDB $unionWith stage operation in aggregation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 23/04/2023
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/unionWith/#mongodb-pipeline-pipe.-unionWith

# Definition
# ----------------------------------------
New in version 4.4.

Performs a union of two collections. 
$unionWith combines pipeline results from two collections into a single result set. The stage outputs the combined result set (including duplicates) to the next stage.

The order in which the combined result set documents are output is unspecified.

# Syntax
# ---------------------------------------
The $unionWith stage has the following syntax:

>>> { $unionWith: { coll: "<collection>", pipeline: [ <stage1>, ... ] } }

To include all documents from the specified collection without any processing, you can use the simplified form:

{ $unionWith: "<collection>" }  // Include all documents from the specified collection

The $unionWith stage takes a document with the following fields:

Field       Description

coll        The collection or view whose pipeline results you wish to include in the result set
pipeline    Optional. An aggregation pipeline to apply to the specified coll.
            [<stage1>, <stage2>, ... ]
            The pipeline cannot include the $out and $merge stages. Starting v6.0, the pipeline can contain
            the Atlas Search $search stage as the first stage inside the pipeline. To learn more, see Atlas Search Support.

The $unionWith operation would correspond to the following SQL statement:

>>> SELECT *
    FROM Collection1
    WHERE ...
    UNION ALL
    SELECT *
    FROM Collection2
    WHERE ...

# Considerations
# ------------------------------

Duplicates Results

The combined results from the previous stage and the $unionWith stage can include duplicates.

For example, create a suppliers collection:

>>> db.suppliers.insertMany([
  { _id: 1, supplier: "Aardvark and Sons", state: "Texas" },
  { _id: 2, supplier: "Bears Run Amok.", state: "Colorado"},
  { _id: 3, supplier: "Squid Mark Inc. ", state: "Rhode Island" },
])

    db.warehouses.insertMany([
  { _id: 1, warehouse: "A", region: "West", state: "California" },
  { _id: 2, warehouse: "B", region: "Central", state: "Colorado"},
  { _id: 3, warehouse: "C", region: "East", state: "Florida" },
])

The following aggregation which combines the results from the state field projection from the suppliers collection with the results from the state field projection from the warehouse collection:

>>> db.suppliers.aggregate([
   { $project: { state: 1, _id: 0 } },
   { $unionWith: { coll: "warehouses", pipeline: [ { $project: { state: 1, _id: 0 } } ]} }
])

As can be seen from the returned documents, the result set contains duplicates:

{ "state" : "Texas" }
{ "state" : "Colorado" }
{ "state" : "Rhode Island" }
{ "state" : "California" }
{ "state" : "Colorado" }
{ "state" : "Florida" }


To remove the duplicats, you can include a $group stage to group by the state field:

>>> db.suppliers.aggregate([
   { $project: { state: 1, _id: 0 } },
   { $unionWith: { coll: "warehouses", pipeline: [ { $project: { state: 1, _id: 0 } } ]} },
   { $group: { _id: "$state" } }
])

The result set no longer contains duplicates:

{ "_id" : "California" }
{ "_id" : "Texas" }
{ "_id" : "Florida" }
{ "_id" : "Colorado" }
{ "_id" : "Rhode Island" }

$unionWith a Sharded Collection

If the $unionWith stage is part of the $lookup pipeline, the $unionWith 
coll cannot be sharded. 
For example, in the following aggregation operation, the inventory_q1 collection cannot be sharded:

>>> db.suppliers.aggregate([
   {
      $lookup: {
         from: "warehouses",
         let: { order_item: "$item", order_qty: "$ordered" },
         pipeline: [
            ...
            { $unionWith: { coll: "inventory_q1", pipeline: [ ... ] } },
            ...
         ],
         as: "stockdata"
      }
   }
])

Collation

If the db.collection.aggregate() includes a collation, that collation is used for the operation, ignoring any other collations.

If the db.collection.aggregate() does not include a collation, the db.collection.aggregate() method uses the collation for the top-level collection/view on which the db.collection.aggregate() is run:

    * If the $unionWith coll is a collection, its collation is ignored.

    * If the $unionWith collis a view, then its collation must match that of the top-level collection/view. Otherwise, the operation errors.

    
Atlas Search Support

Starting in MongoDB 6.0, you can specify the Atlas Search $search or $searchMeta stage in the $unionWith pipeline to search collections on the Atlas cluster. 
The $search or the $searchMeta stage must be the first stage inside the $unionWith pipeline.

[{
  "$unionWith": {
    "coll": <collection-name>,
    "pipeline": [{
      "$search": {
        "<operator>": {
          <operator-specification>
        }
      },
      ...
    }]
  }
}]

To see an example of $unionWith with $search, see the Atlas Search tutorial 
[Run an Atlas Search $search Query Using $unionWith.](https://www.mongodb.com/docs/atlas/atlas-search/tutorial/search-with-unionwith/)

Restrictions

Restriction         Description

Transactions        An aggregation pipeline cannot use $unionWith inside transactions.

Sharded Collection  If the $unionWith stage is part of the $lookup pipeline, 
                    the $unionWith coll cannot be sharded.

$out                The $unionWith pipeline cannot include the $out stage.

$merge              The $unionWith pipeline cannot include the $merge stage.

"""

from typing import Any
from monggregate.base import pyd
from monggregate.base import BaseModel
from monggregate.stages.stage import Stage


class UnionWith(Stage):
    """
    Creates a $unionWith statement in a aggregation pipeline

    Attributes:
    ---------------------------------
        - collection / coll, str : The collection or view whose pipeline results you wish to include in the result set
        - pipeline, list[dict] | Pipeline | None : An aggregation pipeline to apply to the specified coll.
    
    """

    collection : str = pyd.Field(alias="coll")
    # Find a way to better type pipeline while avoiding circular imports <VM, 18/06/2023>
    pipeline : list[dict] | None = None

    @pyd.validator("pipeline", pre=True, always=True)
    def validate_pipeline(cls, pipeline:Any):
        """Validates pipeline"""

        output = pipeline
        if isinstance(pipeline, BaseModel):
            output =  pipeline.statement
        
        return output

    @property
    def statement(self) -> dict[str, dict]:
        """Generates $unionWith statement"""

        if self.pipeline:
            statement = {
                "$unionWith" : {
                    "coll" : self.collection,
                    "pipeline" : self.pipeline
                }
            }
        else:
            statement = {"$unionWith":self.collection}
            
        return self.resolve(statement)
        