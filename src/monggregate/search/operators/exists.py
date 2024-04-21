"""
Module defining an interface to MongoDB Atlas Search exists operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 01/05/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/exists/

# Definition
# --------------------------------------------
The exists operator tests if a path to a specified indexed field name exists in a document. 
If the specified field exists but is not indexed, the document is not included with the result set. 
exists is often used as part of a compound query in conjunction with other search clauses.


# Syntax
# ---------------------------------------------
exists ahs the following syntax:

    >>> {
            $search: {
                "index": <index name>, // optional, defaults to "default"
                "exists": {
                "path": "<field-to-test-for>",
                }
            }
        }

"""

from monggregate.base import Expression
from monggregate.search.operators.operator import SearchOperator

class Exists(SearchOperator):
    """
    Creates an exits operator statement in an Atlas Search query.

    Description:
    ----------------------------------------------
    The exists operator tests if a path to a specified indexed field name exists in a document. 
    If the specified field exists but is not indexed, the document is not included with the result set. 
    exists is often used as part of a compound query in conjunction with other search clauses.

    Attributes:
    ----------------------------------------------

        - path, str : field to test for
 
    """

    path : str # does not allow list


    @property
    def expression(self) -> Expression:
        
        return self.express({
            "exists" : {
                "path":self.path
            }
        })