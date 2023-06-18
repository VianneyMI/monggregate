"""Module definining an interface to MongoDB $searchMeta stage operation in aggregation pipeline.

Online MongoDB documentation:
------------------------------------------------------------

Last Updated (in this package):18/06/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/query-syntax/#definition-1

# Definition
#---------------------------------
The $searchMeta stage returns different types of metadata result documents.

$searchMeta
A $searchMeta pipeline stage has the following prototype form:

    >>> {
            $searchMeta: {
                "index": "<index-name>",
                "<collector-name>"|"<operator-name>": {
                <collector-specification>|<operator-specification>
                },
                "count": {
                <count-options>
                }
            }
        }

# Fields
# ----------------------------------
The $searchMeta stage takes a document with the following fields:

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
# ----------------------------------
The $searchMeta stage must be the first stage in any pipeline.


Metadata Result Types

The structure of the metadata results document that is returned by the $searchMeta stage varies based on the type of results.
Atlas Search supports the following result types:

Type            Result Structure

count           The count result included in the results indicate whether the count returned in the results is a total count of the
                search of results, or a lower bound. To learn more, see Count Results
facet           The result to a facet query is a mapping of the defined facet names to an array of buckets for that facet. To learn
                more, see Facet Results.

"""

from monggregate.stages.search import Search


class SearchMeta(Search):
    """
    Creates a $searchMeta statement in an aggregation pipeline

    Descrtiption
    -----------------------
    The $search stage performs a full-text search on the specified field or fields 
    which must be covered by an Atlas Search index.

    Attributes:
    -----------------------
        - index, str : name of the Atlas Search index to use. Defaults to default.

        - count, dict|None : Document that specifies the count options for retrieving a count
                             of the results. 

        - highlight, dict|None : Document that specifies the highlight options for displaying
                                 search terms in their original context.

        - return_stored_source, bool : Flag that specifies whether to perform a full document lookup
                                       on the backend database (mongod) or return only stored source fields
                                       directly from Atlas Search. Defaults to false.

        - score_details, bool : Flag that specifies whether to retrieve a detailed breakdown of
                                the score for the documents in the results. Defaults to false
                                To view the details, you must use the $meta expression in the
                                $project stage.

        - <operator-name>, dict|None : Name of the operator to search with. You can provide a document
                                  that contains the operator-specific options as the value for this field
                                  Either this or <collector-name> is required.

        - <collector-name>, dict|None : Name of the collector to use with the query. You can provide
                                        a document that contains the collector-specific options as the value
                                        for this field. Either this or <operator-name> is required.
    
    """

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
            "$searchMeta":config
        }
     
        return self.resolve(_statement)
    