"""
Module defining an interface to MongoDB $vectorSearch stage operation in aggrgation pipeline.

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 27/01/2024
Source: https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/

Definition
--------------------------------------------
The $vectorSearch stage performs an aNN search on a vector in the specified field. 
The field that you want to search must be indexed as Atlas Vector Search vector type inside a vectorSearch index type.

A $vectorSearch pipeline has the following prototype form:

{
  "$vectorSearch": {
    "index": "<index-name>",
    "path": "<field-to-search>",
    "queryVector": [<array-of-numbers>],
    "numCandidates": <number-of-candidates>,
    "limit": <number-of-results>,
    "filter": {<filter-specification>}
  }
}

Fields
--------------------------------------------
The $vectorSearch stage takes a document with the following fields:


Field Name	        | Type	    |   Necessity   |   Description

filter              | document	| Optional	    |   Any MQL match expression that compares an indexed field with a boolean, number (not decimals), 
                                                    or string to use as a prefilter. You can use any of the following comparison query and aggregation pipeline
                                                    operators in your filter: $gt, $lt, $gte, $lte, $eq, $ne, $in, $nin, $and, $or
                                                    To learn more, see Atlas Vector Search Pre-Filter(https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/#std-label-vectorSearch-agg-pipeline-filter).

index	            | string	| Required	    |   Name of the Atlas Vector Search index to use.
                                                    Atlas Vector Search doesn't return results if you misspell the index name or if the specified index doesn't already exist on the cluster.

limit	            | number	| Required      |   Number (of type int only) of documents to return in the results. Value can't exceed the value of numCandidates.

numCandidates	    | number	| Required	    |   Number of nearest neighbors to use during the search. Value must be less than or equal to (<=) 10000. 
                                                    You can't specify a number less than the number of documents to return (limit).

                                                    We recommend that you specify a number higher than the number of documents to return (limit) to increase accuracy although this might impact latency. 
                                                    For example, we recommend a ratio of ten to twenty nearest neighbors for a limit of only one document. 
                                                    This overrequest pattern is the recommended way to trade off latency and recall in your aNN searches, and we recommend tuning this on your specific dataset.

path	            | string	| Required	    |   Indexed [vectorEmbedding](https://www.mongodb.com/docs/atlas/atlas-search/field-types/knn-vector/#std-label-fts-data-types-knn-vector) type field to search. 
                                                    To learn more, see [Path Construction](https://www.mongodb.com/docs/atlas/atlas-search/path-construction/#std-label-ref-path).

queryVector	        | array	    | Required	    |   Array of numbers of the BSON double type that represent the query vector. 
                                                    The array size must match the number of vector dimensions specified in the [index definition](https://www.mongodb.com/docs/atlas/atlas-search/field-types/knn-vector/#std-label-fts-data-types-knn-vector) for the field.
                                                    
                                                    # NOTE: You must embed your query with the same model that you used to embed the data


Behavior
--------------------------------------------

$vectorSearch must be the first stage of any pipeline where it appears.

Atlas Vector Search Index

You must index the fields to search using the $vectorSearch stage inside a vectorSearch type index definition. 
You can index the following types of fields in an Atlas Vector Search vectorSearch type index definition:

* Fields that contain vector embeddings as [vector](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type/#std-label-avs-types-vector-search) type
* Fields that contain boolean, numeric, and string values as [filter](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type/#std-label-avs-types-vector-search) type to enable vector search on pre-filtered data.

To learn more about these Atlas Vector Search field types, see [How to Index Fields for Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type/#std-label-avs-types-vector-search).


Atlas Vector Search Score

Atlas Vector Search assigns a score, in a fixed range from 0 to 1 only, to every document that it returns.
For cosine and dotProduct similarities, Atlas Vector Search normalizes the score using the following algorithm:

`score = (1 + cosine/dot_product(v1,v2)) / 2`

The score assigned to a returned document is part of the document's metadata. 
To include each returned document's score along with the result set, use a  $project stage in your aggregation pipeline.

To retrieve the score of your Atlas Vector Search query results, use vectorSearchScore as the value in the $meta expression. 

That is, after the $vectorSearch stage, in the $project stage, the score field takes the [$meta](https://www.mongodb.com/docs/manual/reference/operator/aggregation/meta/) expression. 
The expression requires the vectorSearchScore value to return the score of documents for the vector search.

# NOTE : Pre-filtering your data doesn't affect the score that Atlas Vector Search returns using $vectorSearchScore for $vectorSearch queries.

Atlas Vector Search Pre-Filter

The $vectorSearch filter option matches only BSON boolean, string, and numeric values. 
You must index the fields that you want to filter your data by as the filter type in a vectorSearch type index definition. 
Filtering your data is useful to narrow the scope of your semantic search and ensure that not all vectors are considered for comparison.

The $vectorSearch filter option supports only the following comparison query operators:

* $gt
* $lt
* $gte
* $lte
* $eq** (including the short form version where the operator is ommitted)
* $ne** 
* $in
* $nin

** (Only matches a single value and doesn't support an array of values)

The $vectoSearchnor filter option supports the following comparison aggregation operators:

* $and
* $or

# NOTE : The $vectorSearch filter option doesn't support other comparison query and aggregation pipeline operators.:


# Limitations

$vectorSearch is supported only on Atlas clusters running the following MongoDB versions:

* v6.0.11
* v7.0.2 and later (including RCs).

$vectorSearch can't be used in view definition and the following pipeline stages:

* $lookup sub-pipeline ** 
* $unionWith sub-pipeline **
* $facet pipeline stage

** (You can pass the results of $vectorSearch to this page).

Supported Clients

You can run $vectorSearch queries using the Atlas Data Explorer, mongosh, and the following drivers:

* C#
* Java
* Node
* Pymongo

You can also use Atlas Vector Search with local Atlas deployments that you create with the Atlas CLI.
To learn more, see [Create a Local Atlas Deployment](https://www.mongodb.com/docs/atlas/cli/stable/atlas-cli-deploy-local/)


"""

from monggregate.base import pyd
from monggregate.stages.stage import Stage

class VectorSearch(Stage):
    """
    Abstration of MongoDB $vectorSearch statement that performs an aNN search on a vector in the specified field.

    Attributes:
    -----------

        - index, str : name of the Atlas Vector Search index to use
        - path, str : path to the vector field to search
        - query_vector, list[float] : array of numbers of the BSON double type that represent the query vector
        - num_candidates, int : number of nearest neighbors to use during the search
        - limit, int : number of documents to return in the results
        - filter, dict|None : any MQL match expression that compares an indexed field with a boolean, number (not decimals), or string to use as a prefilter
    
    """

    filter : dict|None
    index : str
    limit : int = pyd.Field(le=10000)
    num_candidates : int
    path : str
    query_vector : list[float]

    @pyd.validator("num_candidates", pre=True, always=True)
    def validate_num_candidates(cls, num_candidates:int, values:dict):
        """Validates that num_candidates is less than or equal to 10000"""
    
        limit:int = values.get("limit", 1)
        if limit >= num_candidates:
            raise ValueError("num_candidates must be greater than limit")
        
        return num_candidates
    
    @property
    def statement(self) -> dict[str, dict]:
        """Generates set stage statement from arguments"""

        return self.resolve({"$vectorSearch" : {
            "index" : self.index,
            "path" : self.path,
            "queryVector" : self.query_vector,
            "numCandidates" : self.num_candidates,
            "limit" : self.limit,
            "filter" : self.filter
        }})
    