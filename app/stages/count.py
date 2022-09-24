"""
Module definining an interface to MongoDB $count stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 18/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/count/#mongodb-pipeline-pipe.-count

Definition
-------------------

Passes a document to the next stage that contains a count of the number of documents input to the stage.

$count has the following prototype form:
   >>> {"$count":"string"}

<string> is the name of the output field which has the count as its value.
<string> must be a non-empty string, must not start with $ and must not contain the . character.


Behavior
-------------------
The $count stage is equivalent to the following
$group + $project sequence:

   >>>  db.collection.aggregate([
            { $group: { _id: null, myCount: { $sum: 1 } } },
            { $project: { _id: 0 } }
        ])

where myCount would be the output field that contains the count. You can specify another name for the output field.


"""

from pydantic import root_validator
from app.stages.stage import Stage

class Count(Stage):
    """
    Creates a count statement for an aggregation pipeline count stage

    Attributes
    -------------------------------

        - name, str : name of the output field which the count as its value.
                      Must be a non-empty string,
                      NOTE : Must not start with $ and must not contain the
                             . character.

    """

    name : str


    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        # Retrieving the values
        #---------------------------------------
        name = values.get("name")
        if not name:
            raise TypeError("name is required")

        values["_statement"] = {
            "$count" : name
        }

        return values