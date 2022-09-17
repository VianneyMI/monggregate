"""
Module definining an interface to MongoDB $bucketAuto stage operation in aggrgation pipeline

"""

from pydantic import root_validator, Field
from app.stages.stage import Stage

class Bucket(Stage):
    """
    TBD

    """

    statement: dict
    by : str = Field(...,alias="group_by")
    buckets : list
    output : dict

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict:
        """Generates statement from arguments"""

        by = values.get("by")
        #group_by

        buckets = values.get("buckets")
        output = values.get("output")
        granularity = values.get("granularity")

        # Handling aliases
        #--------------------------------------

        values["statement"] = {
            "$bucketAuto" : {
                "groupBy" : by,
                "buckets" : buckets,
                "output" : output,
                "ganularity" : granularity
            }
        }

        return values
