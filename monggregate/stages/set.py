"""
Module definining an interface to MongoDB $set stage operation in aggregation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 20/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/set/#mongodb-pipeline-pipe.-set


# Definition
# --------------------------------

Adds new fields to documents. $set outputs documents that conain all existing fields from the inputs documents
and newly added fields.

The $set stage is an alias for $addFields.

Both stages are equivalent to a $project stage that explicitly specifies all existing fields in the inputs documents and adds the new fields.

$set has the following form:

    >>> { $set: { <newField>: <expression>, ... } }

Specify the name of each field to add and set its value to an aggregation expression. For more information on expressions, see Expressions.

$set appends new fields to existing documents. You can include one or more $set stages in an aggregation operation.

To add field or fields to embedded documents (including documents in arrays) use the dot notation.
See example : https://www.mongodb.com/docs/manual/reference/operator/aggregation/set/#std-label-set-add-field-to-embedded

To add an element to an existing array field with $set, use with $concatArrays.
See example : https://www.mongodb.com/docs/manual/reference/operator/aggregation/set/#std-label-set-add-element-to-array

"""

from monggregate.stages.stage import Stage

class Set(Stage):
    """
    Creates a set statement for a pipeline set aggregation stage

    Attributes:
    ---------------------------------
        - statement, dict :
        - document, dict : new fields to be added

    """

    document : dict = {} #| None

    @property
    def statement(self)->dict[str, dict]:
        """Generates set stage statement from arguments"""

        return  self.resolve({"$set":self.document})
