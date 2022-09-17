"""
Module defining an interface to MongoDB $match stage operation in aggregation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 16/09/2022
Source :  https://www.mongodb.com/docs/manual/meta/aggregation-quick-reference/

Filters the documents to pass only the documents that match the specified condition(s) to the next pipeline stage.

The  $match stage has the following prototype form:
    >>> { $match: { <query> } }


$match takes a document that specifies the query conditions. The query syntax is identical to the read operation query syntax; i.e.
$match does not accept raw aggregation expressions. Instead, use a $expr query expression to include aggregation expression in
$match

Behavior
------------
Pipeline Optimization
----------------------
    * Place the  $match as early in the aggregation pipeline as possible. Because
        $match limits the total number of documents in the aggregation pipeline, earlier
        $match operations minimize the amount of processing down the pipe.

    * If you place a $match at the very beginning of a pipeline, the query can take advantage of indexes like any other
      db.collection.find() or  db.collection.findOne().

Restrictions
--------------------
    * The $match query syntax is identical to the read operation query syntax; i.e.
     $match does not accept raw aggregation expressions. To include aggregation expression in
     $match, use a $expr query expression:
    >>> { $match: { $expr: { <aggregation expression> } } }

    * You cannot use $where in $match queries as part of the aggregation pipeline.
    * You cannot use $where in $match queries as part of the aggregation pipeline.
    * You cannot use $near or $nearSphere in $match queries as part of the aggregation pipeline.
      As an alternative, you can either:
        * Use $geoNear stage instead of the $match stage.
        * Use *geoWithin query operator with $center or $centerSphere in the $match stage.
    * To use $text in the $match stage, the $match stage has to be the first stage of the pipeline.

"""

from pydantic import root_validator
from app.stages.stage import Stage

class Match(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    query : dict ={} #| None

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates match stage statement from arguments"""

        query = values.get("query")
        values["statement"] = {"$match":query}

        return values
