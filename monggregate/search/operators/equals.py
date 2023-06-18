"""
Module defining an interface to MongoDB Atlas Search operator autcomplete

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 30/04/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/equals/

# Definition
# --------------------------------------------

The equals operator checks whether a field matches a value you specify. equals supports querying the following data types:

    * boolean
    * objectId
    * number, including int32, int64, and double
    * date

You can use the equals operator to query booleans, objectIds, numbers, and dates in arrays. 
If at least one element in the array matches the "value" field in the equals operator, Atlas Search adds the document to the result set.

NOTE : The equals operator supports numbers up to 15 decimal digits. 
       Additional decimal digits in documents or queries can cause precision issues or query inaccuracy.

# Syntax
# ----------------------------------------------

equals has the following syntax:

    >>> {
            $search: {
                "index": <index name>, // optional, defaults to "default"
                "equals": {
                    "path": "<field-to-search>",
                    "value": <boolean-value>|<objectId>|<number>|<date>,
                    "score": <score-options>
                }
            }
        }

# Options
# ---------------------------------------------

Field       Type            Description                             Necessity

path        string          Indexed field to search.                 Yes

value       boolean,        Value to query for.                      Yes
            objectId,
            number,
            date

score       object          Score assigned to matching search        No 
                            term results. Use one of the following
                            options to modify the score:
                                * boost : multiply the score by 
                                          the given number
                                * constant : replace the result
                                             score with the given
                                             number

# Behavior
# ---------------------------------------------

equals uses constant scoring. 
Each matching document receives a score of 1 for each search clause matched. 
A document that matches one search clause receives a score of 1, while a document that matches three search clauses receives a score of 3. 

"""

from datetime import datetime
from monggregate.search.operators.operator import SearchOperator

class Equals(SearchOperator, smart_union=True):
    """
    Creates an equals operation statement in an Atlas Search query.

    Description:
    ----------------------------------------------
    The equals operator checks whether a field matches a value you specify. 

    Attributes:
    ----------------------------------------------
        - path, str : Indexed field to search.
        - value, str | int | float | bool | datetime : Value to query for.
        - score, dict : Score assigned to matching search term results. 
                        Use one of the following options to modify the score:
                            * boost : multiply the score by the given number
                            * constant : replace the result score with the given number


    """

    path : str # does not allow list
    value : str | int | float | bool | datetime 
    score : dict|None

    @property
    def statement(self) -> dict:
            
            return self.resolve({
                "equals":{
                    "path": self.path,
                    "value": self.value,
                    "score": self.score
                }
            })
    