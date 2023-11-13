"""
Module defining an interface to MongoDB $match stage operation in aggregation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 16/09/2022
Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match

Definition
---------------------
Filters the documents to pass only the documents that match the specified condition(s) to the next pipeline stage.

The  $match stage has the following prototype form:
    >>> { $match: { <query> } }


$match takes a document that specifies the query conditions. The query syntax is identical to the read operation query syntax; i.e.
$match does not accept raw aggregation expressions. Instead, use a $expr query expression to include aggregation expression in
$match

Behavior
----------------------
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

from typing import Any

from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.operators.operator import Operator
from monggregate.expressions import Expression

class Match(Stage):
    """
    Abstraction of MongoDB $match statement that filters the documents to pass to the next pipeline stage based on the specified condition(s).

    Attributes:
    -----------

        - query, dict : a simple MQL query use to filter the documents.
        - expression, Expression : an aggregation expression used to filter the documents
    
    NOTE : Use query if you're using a MQL query and expression if you're using aggregation expressions.
    
    
    Online MongoDB documentation:
    -----------------------------
    Filters the documents to pass only the documents that match the specified condition(s) to the next pipeline stage.
    
    $match takes a document that specifies the query conditions. The query syntax is identical to the read operation query syntax; i.e.
    $match does not accept raw aggregation expressions. Instead, use a $expr query expression to include aggregation expression in
    $match

    Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match
    """

    query : dict = {} #| None
    expression : Any | None = None

    @pyd.validator("expression", pre=True, always=True)
    def validate_expression(cls, expression)-> Any:
        
        c1 = isinstance(expression, dict) # expression is "expressed/resolved" already
        c2 = isinstance(expression, Expression) # expression is an expression object
        c3 = isinstance(expression, Operator) # expression is an operator object

        if expression and not (c1 or c2 or c3):
            raise ValueError("The expression argument must be a valid expression, operator or a dict.")
        
        return expression

    @property
    def statement(self) -> dict:

        if self.expression:
            _statement = self.resolve({"$match":{"$expr":self.expression}})
            
        else:
            _statement =  self.resolve({"$match":self.query})

        return _statement
