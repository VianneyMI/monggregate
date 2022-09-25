"""
Module definining an interface to MongoDB $replaceRoot stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 20/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#mongodb-pipeline-pipe.-replaceRoot

Definition
----------------------------
Replaces the input document with the specified document.
The operation replaces all existing fields in the input document, including the _id field.
You can promote an existing embedded document to the top level, or create a new document for promotion
(see example:https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#std-label-new-replacement-doc).

The $replaceRoot stage has the following form:

    >>> { $replaceRoot: { newRoot: <replacementDocument> } }

The replacement document can be any valid expression that resolves to a document.
The stage errors and fails if <replacementDocument> is not a document. For more information on expressions, see Expressions.

Behavior
----------------------------
If the <replacementDocument> is not a document, $replaceRooterrors and fails.

If the <replacementDocument> resolves to a missing document (i.e. the document does not exist),
$replaceRooterrors and fails. For example, create a collection with the following documents:

    >>> db.collection.insertMany([
            { "_id": 1, "name" : { "first" : "John", "last" : "Backus" } },
            { "_id": 2, "name" : { "first" : "John", "last" : "McCarthy" } },
            { "_id": 3, "name": { "first" : "Grace", "last" : "Hopper" } },
            { "_id": 4, "firstname": "Ole-Johan", "lastname" : "Dahl" },
        ])

Then the following $replaceRoot operation fails because one of the documents does not have the name field:

    >>> db.collection.aggregate([
            { $replaceRoot: { newRoot: "$name" } }
        ])

To avoid the error, you can use $mergeObjects to merge the name document into some default document; for example:

    >>> db.collection.aggregate([
            { $replaceRoot: { newRoot: { $mergeObjects: [ { _id: "$_id", first: "", last: "" }, "$name" ] } } }
        ])

Alternatively, you can skip the documents that are missing the name field by including a $match stage to check for existence of the document field
before passing documents to the $replaceRoot stage:

    >>> db.collection.aggregate([
            $match: { name : { $exists: true, $not: { $type: "array" }, $type: "object" } } },
            { $replaceRoot: { newRoot: "$name" } }
        ])

Or, you can use $ifNullexpression to specify some other document to be root; for example:

    >>> db.collection.aggregate([
            { $replaceRoot: { newRoot: { $ifNull: [ "$name", { _id: "$_id", missingName: true} ] } } }
        ])



"""

from pydantic import root_validator, Field
from app.stages.stage import Stage


class ReplaceRoot(Stage):
    """
    Creates a replace root statement for an aggregation pipeline replace root stage.

    Attributes:
    ---------------------------

        - statement, dict : the statement generated during instantiation after parsing the other arguments
        - path_to_new_root, str : the path to the embedded document to be promoted
        - document, dict : documents being created and to be set as the new root (Not implemented yet)

    """

    path_to_new_root : str = Field(..., alias="path")
    #document : dict

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict:
        """Generate statements from argument"""

        path_to_new_root:str|None = values.get("path_to_new_root")
        path = values.get("path")

        if not path_to_new_root:
            path_to_new_root = path

        if not path_to_new_root.startswith("$"):
            path_to_new_root = "$" + path_to_new_root


        values["statement"] = {"$replaceRoot":{"newRoot":path_to_new_root}}

        return values

    # TODO : Add validator to check path/path_to_new_root correctness <VM, 25/09/2022>