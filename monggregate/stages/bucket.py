"""
Module definining an interface to MongoDB $bucket stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 18/09/2022
Source :  https://www.mongodb.com/docs/manual/meta/aggregation-quick-reference/

Definition
--------------------

Categorizes incoming documents into groups, called buckets, based on a specified expression and bucket boundaries and outputs a document per each bucket. Each output document contains an _id field whose value specifies the inclusive lower bound of the bucket. The
output option specifies the fields included in each output document.

$bucket only produces output documents for buckets that contain at least one input document.

Considerations
--------------------
The $bucket stage has a limit of 100 megabytes of RAM. By default, if the stage exceeds this limit,
$bucket returns an error. To allow more space for stage processing, use the allowDiskUse option to enable aggregation pipeline stages to write data to temporary files.

Syntax
--------------------
{
  $bucket: {
      groupBy: <expression>,
      boundaries: [ <lowerbound1>, <lowerbound2>, ... ],
      default: <literal>,
      output: {
         <output1>: { <$accumulator expression> },
         ...
         <outputN>: { <$accumulator expression> }
      }
   }
}

Behavior
-------------------
$bucket requires at least one of the following conditions to be met or the operation throws an error:

    * Each input document resolves the groupBy expression to a value within one of the bucket ranges specified by
boundaries, or

    * A default value is specified to bucket documents whose groupBy values are outside of the boundaries or of a different BSON type than the values in boundaries.

If the groupBy expression resolves to an array or a document, $bucket arranges the input documents into buckets using the comparison logic from
$sort.

"""

from typing import Any

from monggregate.base import pyd

from monggregate.stages.stage import Stage
from monggregate.fields import FieldName
from monggregate.operators.accumulators.accumulator import AccumulatorExpression
from monggregate.utils import validate_field_path

class Bucket(Stage):
    """
    Creates a bucket statement for an aggregation pipeline bucket stage.
    This stage aggregates documents into buckets specified by the boundaries argument.

    Attributes:
    ---------------------------------
        by : str|list[str]|set[str], field or fields to group the documents
                                     unless a default is provided, each input document
                                     must resolve the groupBy field path or expression
                                     to a value that falls within one of the ranges specified
                                     by the boundaries
        boundaries : list, an array of values that specify the boundaries for each bucket.
                           Each adjacent pair of values acts as the inclusive lower boundary
                           and the exclusive upper boundary for the bucket.
                           NOTE : You must specify at least two boundaries.
        default : Any, Optional. A literal that specifies the _id (group name) of an additional
                                 bucket that contains all documents whoe groupBy expression result
                                 does not fall into a bucket specified by the boundaries

                                 If unspecified, each input document must resolve groupBy
                                 expression to a value within one of the bucket ranges.

                                 The default value must be less than the lowest boundary or greather
                                 than or equal to the highest boundary value

                                 The default value can be of a different type than the entries in boundaries
        output : dict | None, A document that specifies the fields to include in the output documents in addition to
                              the _id field. To specify the field to include you must use accumulator expressions
                                 >>> {"outputField1" : {"accumulator":"expression1}}
                                      ....
                                     {"outputField2" : {"accumulator":"expression2}}
                              If you do not specify an output document, the operation returns a count field containing
                              the number of documents in each bucket.

                              If you specify and output document, only the fields specified in the document are returned; i.e.
                              the count field is not returned unless it is explicitly included in the output document

    """

    by : Any = pyd.Field(...,alias="group_by")
    boundaries : list
    default : Any = None
    output : dict[FieldName, AccumulatorExpression] | None = None

    # Validators
    # ------------------------------
    _validate_by = pyd.validator("by", pre=True, always=True, allow_reuse=True)(validate_field_path) # re-used pyd.validators

    @property
    def statement(self) -> dict:

        # Generates statement
        #--------------------------------------
        return self.resolve({
            "$bucket" : {
                "groupBy" : self.by,
                "boundaries" :self.boundaries,
                "default" : self.default,
                "output" : self.output
            }
        })
