"""
Module defining an interface to MongoDB `$count` stage operation in aggregation pipeline.
"""

from monggregate.stages.stage import Stage
from monggregate.fields import FieldName

class Count(Stage):
    """
    Abstraction of MongoDB `$count` statement that counts the number of 
    documents input to the stage.

    Parameters
    ----------
    - name, str
        Name of the output field which the count as its value.
        Must be a non-empty string, must not start with `$`, and must not 
        contain the `.` character.

                  
    Online MongoDB documentation:
    -----------------------------
    Passes a document to the next stage that contains a count of the number of documents input to the stage.

    `$count` has the following prototype form:
    
        >>> {"$count":"string"}

    `<string>` is the name of the output field which has the count as its value.
    `<string>` must be a non-empty string, must not start with `$` and must not contain the `.` character.
    
    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/count/)
    """

    name: FieldName

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$count": self.name
        })
