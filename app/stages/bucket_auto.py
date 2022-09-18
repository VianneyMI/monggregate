"""
Module definining an interface to MongoDB $bucketAuto stage operation in aggrgation pipeline

"""

from pydantic import root_validator, Field
from app.stages.stage import Stage
from app.utils import StrEnum

class GranularityEnum(StrEnum):
    """Supported values of granularity are"""

    R5 = "R5"
    R10 = "R10"
    R20 = "R20"
    R40 = "R40"
    R80 = "R80"
    _1_2_5 = "1-2-5"
    E6 = "E6"
    E12 = "E12"
    E24 = "E24"
    E48 = "E48"
    E96 = "E96"
    E192 = "E192"
    POWERSOF2 = "POWERSOF2"

class BucketAuto(Stage):
    """
    Creates a bucket statement for an aggregation pipeline bucket stage.
    This stage aggregates documents into buckets automatically computed to statisfy the number of buckets desired
    and provided as an input.

    Attributes
    -----------------
        by : str|list[str]|set[str], An expression to group documents. To specify a field path
                                     prefix the field name with a dollar sign $ and enclose it in quotes.
        buckets : int, number of buckets desired
        output : dict, A document that specifieds the fields to include in the oupput documents in addition
                       to the _id field. To specify the field to include, you must use accumulator expressions.

                       The defaut count field is not included in the output document when output is specified. Explicitly specify the count expression
                       as part of the output document to include it:

                       >>> {
                                <outputfield1>: { <accumulator>: <expression1> },
                                ...
                                count: { $sum: 1 }
                           }
        granularity : str | None

    """

    statement: dict
    by : str = Field(...,alias="group_by")
    buckets : int
    output : dict
    granularity : str

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
