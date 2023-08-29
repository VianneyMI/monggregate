"""
Module definining an interface to MongoDB $bucketAuto stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 16/09/2022
Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/bucketAuto/


Definition
---------------------
Categorizes incoming documents into a specific number of groups, called buckets, based on a specified expression.
Bucket boundaries are automatically determined in an attempt to evenly distribute the documents into the specified number of buckets.

Each bucket is represented as a document in the output. The document for each bucket contains:

    * An _id object that specifies the bounds of the bucket.

        * The _id.min field specifies the inclusive lower bound for the bucket.

        * The _id.max field specifies the upper bound for the bucket. This bound is exclusive for all buckets except the final bucket in the series, where it is inclusive.

    * A count field that contains the number of documents in the bucket. The count field is included by default when the output document is not specified.

The $bucketAuto stage has the following form:

    >>> {
            $bucketAuto: {
                groupBy: <expression>,
                buckets: <number>,
                output: {
                    <output1>: { <$accumulator expression> },
                    ...
                }
                granularity: <string>
            }
        }

Considerations
------------------------
The $bucketAuto stage has a limit of 100 megabytes of RAM. By default, if the stage exceeds this limit,
$bucketAuto returns an error. To allow more space for stage processing, use the allowDiskUse option to enable aggregation pipeline stages to write data to temporary files.

Behavior
-----------------------
There may be less than the specified number of buckets if:

    * The number of input documents is less than the specified number of buckets.

    * The number of unique values of the groupBy expression is less than the specified number of buckets.

    * The granularity has fewer intervals than the number of buckets.

    * The granularity is not fine enough to evenly distribute documents into the specified number of buckets.

If the groupBy expression refers to an array or document, the values are arranged using the same ordering as in
$sort before determining the bucket boundaries.

The even distribution of documents across buckets depends on the cardinality, or the number of unique values, of the groupBy field.
If the cardinality is not high enough, the $bucketAuto stage may not evenly distribute the results across buckets.

Granularity
-----------------

The $bucketAuto accepts an optional granularity parameter which ensures that the boundaries of all buckets adhere to a specified
preferred number series.
Using a preferred number series provides more control on where the bucket boundaries are set among the range of values in the groupBy expression.
They may also be used to help logarithmically and evenly set bucket boundaries when the range of the groupBy expression scales exponentially.

Renard Series

The Renard number series are sets of numbers derived by taking either the 5 th, 10 th, 20 th, 40 th, or 80 th root of 10,
then including various powers of the root that equate to values between 1.0 to 10.0 (10.3 in the case of R80).

Set granularity to R5, R10, R20, R40, or R80 to restrict bucket boundaries to values in the series.
The values of the series are multiplied by a power of 10 when the groupBy values are outside of the 1.0 to 10.0 (10.3 for R80) range.



"""

from typing import Any
from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.fields import FieldName
from monggregate.operators.accumulators.accumulator import AccumulatorExpression
from monggregate.utils import StrEnum, validate_field_path

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

    Attributes:
    ---------------------------------
        by : str|list[str]|set[str], An expression to group documents. To specify a field path
                                     prefix the field name with a dollar sign $ and enclose it in quotes.
        buckets : int, number of buckets desired
        output : dict, A document that specifieds the fields to include in the oupput documents in addition
                       to the _id field. To specify the field to include, you must use accumulator expressions.

                       The defaut count field is not included in the output document when output is specified.
                       Explicitly specify the count expression as part of the output document to include it:

                       >>> {
                                <outputfield1>: { <accumulator>: <expression1> },
                                ...
                                count: { $sum: 1 }
                           }
        granularity : str | None, A string that specifies the preferred number series to use to ensure that the calculated
                                  boundary edges end on preferred round numbers of their powers of 10.

                                  Available only if the all groupBy values are numeric and none of them are NaN.
                                  https://en.wikipedia.org/wiki/Preferred_number

    """

    # Attributes
    # ----------------------------------------------------------------------------
    by : Any = pyd.Field(...,alias="group_by") # probably should restrict type to field_paths an operator expressions
    buckets : int = pyd.Field(..., gt=0)
    output : dict[FieldName, AccumulatorExpression] | None = None# Accumulator Expressions #TODO : Define type and use it here
    granularity : GranularityEnum | None = None


    # Validators
    # ----------------------------------------------------------------------------
    _validate_by = pyd.validator("by", pre=True, always=True, allow_reuse=True)(validate_field_path) # re-used pyd.validators

    # Output
    #-----------------------------------------------------------------------------
    @property
    def statement(self) -> dict:

      # NOTE : maybe it would be better to use _to_unique_list here
      # or to further validate by.
      return   self.resolve({
            "$bucketAuto" : {
                "groupBy" : self.by,
                "buckets" : self.buckets,
                "output" : self.output,
                "granularity" : self.granularity.value if self.granularity else None
            }
        })
