"""
Module defining an interface to MongoDB $project stage operation in aggregation pipeline

Online MongoDB documentation:
---------------------------------------------------------------------------------------
Last Updated :
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project

Definition
----------------------------

Passes along the documents with the requested fields to the next stage in the pipeline. The specified fields can be existing fields from the input documents or newly computed fields.

The $project stage has the following prototype form:

    >>> { $project: { <specification(s)> } }


The $project takes a document that can specify the inclusion of fields,
the suppression of the _id field, the addition of new fields, and the resetting of the values of existing fields. Alternatively, you may specify the exclusion of fields.

The $project specifications have the following forms:
See class definition below

Considerations
------------------------------

Include Existing Fields

    * The _id field is, by default, included in the output documents. To include any other fields from the input documents in the output documents,
      you must explicitly specify the inclusion in $project.

    * If you specify an inclusion of a field that does not exist in the document, $project ignores that field inclusion and does not add the field to the document.

Suppress the _id Field

By default, the _id field is included in the output documents. To exclude the _id field from the output documents, you must explicitly specify the suppression of the _id field in
$project.

Exclude Fields

If you specify the exclusion of a field or fields, all other fields are returned in the output documents.

    >>> { $project: { "<field1>": 0, "<field2>": 0, ... } } // Return all but the specified fields

If you specify the exclusion of a field other than _id, you cannot employ any other $project
specification forms: i.e. if you exclude fields, you cannot also specify the inclusion of fields,
reset the value of existing fields, or add new fields. This restriction does not apply to conditional exclusion of a field using the
REMOVE variable.

See also the $unset stage to exclude fields.

Exclude Fields Conditionally

You can use the variable REMOVE in aggregation expressions to conditionally suppress a field.
For an example, see Conditionally Exclude Fields: https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#std-label-remove-example

Add New Fields or Reset Existing Fields

# NOTE : MongoDB also provides $addFields to add new fields to the documents.

To add a new field or to reset the value of an existing field, specify the field name and set its value to some expression.
For more information on expressions, see Expressions.

Literal Values

To set a field value directly to a numeric or boolean literal, as opposed to setting the field to an expression that resolves to a literal, use the
$literal operator. Otherwise, $project treats the numeric or boolean literal as a flag for including or excluding the field.

Field Rename

By specifying a new field and setting its value to the field path of an existing field, you can effectively rename a field.

New Array Fields

The $project stage supports using the square brackets [] to directly create new array fields. If you specify array fields that do not exist in a document,
the operation substitutes null as the value for that field.
For an example, see Project New Array Fields : https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#std-label-example-project-new-array-fields

You cannot use an array index with the $project stage.
See Array Indexes are Unsupported : https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#std-label-example-project-array-indexes

Embedded Document Fields

When projecting or adding/resetting a field within an embedded document, you can either use dot notation, as in

    >>> "contact.address.country": <1 or 0 or expression>

Or you can nest the fields:

    >>> contact: { address: { country: <1 or 0 or expression> } }

When nesting the fields, you cannot use dot notation inside the embedded document to specify the field, e.g. contact: { "address.country": <1 or 0 or expression> } is invalid.

Path Collision Erros in Embedded Fields

You cannot specify both an embedded document and a field within that embedded document in the same projection.

The following $project stage fails with a Path collision error because it attempts to project both the embedded contact document and the contact.address.country field:

    >>> { $project: { contact: 1, "contact.address.country": 1 } }

The error occurs regardless of the order in which the parent document and embedded field are specified.
The following $project fails with the same error:

    >>> { $project: { "contact.address.country": 1, contact: 1 } }

Restrictions
-----------------------------------

An error is returned if the
$project
 specification is an empty document.

You cannot use an array index with the
$projectstage. See Array Indexes are Unsupported.


"""

# NOTE : This is a first prototype, there are so much that can be done by $project that this will be completed
# after further reading the doc and copying here and
# after having prototype more stages

# NOTE : Would be nice and useful to have something keywords arguments based to generate the projection <VM, 16/09/2022>
# (on top[on the side] of the below)
from pydantic import root_validator

from monggregate.stages.stage import Stage

class Project(Stage):
    """"
    Creates a project statement for an aggregation pipeline project stage.

    Attributes:
    ---------------------------
        - projection, dict | None : projection to be applied
        - include, str | list[str] | set[str] | dict | None : fields to be kept
        - exclude, str | list[str] | set[str] | dict | None : fields to be excluded

    """

    projection : dict | None
    include : set[str] | dict | None # TODO : Allow str and list[str] also
    exclude : set[str] | dict | None # TODO : Allow str and list[str] also

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates statelent from other attributes"""


        def _parse_include_exclude(include_or_exclude:set[str]|dict|None, required:bool)->tuple[dict, bool]:
            """Parses include and exclude arguments"""

            projection = {}
            is_valid = False
            if include_or_exclude and len(include_or_exclude)>0:
                is_valid = True

                if isinstance(include_or_exclude, set):
                    for field in include_or_exclude:
                        projection[field] = required
                else:
                    projection.update(include_or_exclude)


            return projection, is_valid

        projection = values.get("projection")
        include = values.get("include")
        exclude = values.get("exclude")

        if not (projection or include or exclude):
            raise TypeError("At least one of (projection, include, exclude) is required")

        if not projection:
            include_projection, is_include_valid = _parse_include_exclude(include, True)
            exclude_projection, is_exclude_valid = _parse_include_exclude(exclude, False)

            print("include_projection: ", include_projection)
            print("exclude_projection", exclude_projection)

            projection = include_projection | exclude_projection
            is_valid = is_include_valid or is_exclude_valid

            if not is_valid:
                raise ValueError("At least one of (include, exclude) must be valid when projection is not provided")


        values["statement"] = {"$project":projection}

        return values
