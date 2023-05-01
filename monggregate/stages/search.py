"""Module definining an interface to MongoDB $limit stage operation in aggrgation pipeline.

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------

Last Updated (in this package) : 25/04/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/query-syntax/#mongodb-pipeline-pipe.-search

# Definition
#---------------------------
The $search stage performs a full-text search on the specified field or fields which must be covered by an Atlas Search index.

$search
A $search pipeline stage has the following prototype form:

    >>> {
            $search: {
                "index": "<index-name>",
                "<operator-name>"|"<collector-name>": {
                <operator-specification>|<collector-specification>
                },
                "highlight": {
                <highlight-options>
                },
                "count": {
                <count-options>
                },
                "returnStoredSource": true | false
            }
        }

# Fields
#---------------------------

The $search stage takes a document with the following fields

Field                       Type       Necessity       Description

<collector-name>            document   Conditional     Name of the collector to use with the query. 
                                                       You can provide a document that contains the collector-specific options as the value for this field. 
                                                       Either this or <operator-name> is required.
count                       document   Optional        Document that specifies the count options for retrieving a count of the results. 
                                                       To learn more, see Count Atlas Search Results.
highlight                   document   Optional        Document that specifies the highlight options for displaying search terms in their original context.
index                       string     Required        Name of the Atlas Search index to use. If omitted, defaults to default
<operator-name>             document   Conditional     Name of the operator to search with. 
                                                       You can provide a document that contains the operator-specific options as the value for this field. 
                                                       Either this or <collector-name> is required.
returnStoredSource          boolean    Optional        Flag that specifies whether to perform a full document lookup on the backend database or return only stored source fields directly from Atlas Search. 
                                                       If omitted, defaults to false. To learn more, see Return Stored Source Fields.

# Behavior
#---------------------------
$search must be the first stage of any pipeline it appears in. 
$search cannot be used in:

    * a view definition

    * a $facet pipeline stage

# Aggregation Variable
#---------------------------
$search returns only the results of your query. The metadata results of your 
$search query are saved in the $$SEARCH_META aggregation variable. You can use the $$SEARCH_META variable to view the metadata results for your 
$search query. The $$SEARCH_META aggregation variable can be used anywhere after a 
$search stage in any pipeline, but it can't be used after the $lookup or $unionWith stage in any pipeline. 
The $$SEARCH_META aggregation variable can't be used in any subsequent stage after a $searchMeta stage.
                                                       
"""

from pydantic import Field, validator
from monggregate.stages.stage import Stage

class Search(Stage):
    """"xxx"""

    index : str = "default"
    count : dict|None
    highlight : dict|None
    collector : dict|None
    operator : dict|None
    return_stored_source : bool = Field(False, alias="returnStoredSource")
    score_details : bool = Field(False, alias="scoreDetails")

    @validator("operator", pre=True, always=True)
    @classmethod
    def validate_operator(cls, value:dict, values:dict)->dict|None:
        """Ensures that either collector or operator is provided"""

        collector = values.get("collector")
        if not collector and not value:
            raise TypeError("Either collector or operator must be provided")
        
        return value
    
    @property
    def statement(self) -> dict[str, dict]:
    
        config = {
                "index":self.index,
                "highlight":self.highlight,
                "count":self.count,
                "returnStoredSource":self.return_stored_source,
                "scoreDetails":self.score_details
            }
        
        method:dict[str, dict] = self.collector or self.operator

        config.update(method)

        _statement = {
            "$search":config
        }
     
        return _statement