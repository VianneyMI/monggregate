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

from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.utils import to_unique_list

ProjectionArgs = str | list[str] | set[str]

class Project(Stage):
    """"
    Creates a project statement for an aggregation pipeline project stage.

    Attributes:
    ---------------------------
        - projection, dict | None : projection to be applied
        - fields, ProjectionArgs | None : fields  to be kept or excluded (depending on include/exclude parameters when those are booleans)
        - include, ProjectionArgs| dict | bool | None : fields to be kept
        - exclude, ProjectionArgs | dict | bool | None : fields to be excluded

    """

    include : list[str] | dict | bool | None = None
    exclude : list[str] | dict | bool | None = None
    fields : list[str] | None = None
    projection : dict = {}

    @pyd.validator("include", "exclude", pre=True, always=True)
    @classmethod
    def parse_include_exclude(cls, value:ProjectionArgs|dict|bool|None)->list[str]|dict|bool|None:
        """Parses include and exclude arguments"""

        return to_unique_list(value)

    @pyd.validator("exclude")
    @classmethod
    def validates_booleans(cls, exclude:ProjectionArgs|dict|bool|None, values:dict[str, ProjectionArgs|dict|bool|None]) -> list[str]|bool|None:
        """Validates combination of include and exclude"""

        include = values.get("include")
        if isinstance(include, bool) and isinstance(exclude, bool):
            raise ValueError("Cannot both include and exclude fields when using include and exlude as booleans")

        return exclude

    # TODO : When using fields, consider include = True as default
    @pyd.validator("fields", pre=True)
    @classmethod
    def validates_fields(cls, value:ProjectionArgs|None, values:dict[str, list[str]|dict|bool|None])-> list[str]|None:
        """Validates fields"""

        include = values.get("include")
        exclude = values.get("exclude")

        if value and not (isinstance(include, bool) or isinstance(exclude, bool)):
            raise ValueError("Either include or exclude must be set and be a boolean when using fields")

        fields = to_unique_list(value)
        return fields


    @pyd.validator("projection", pre=True, always=True)
    @classmethod
    def generates_projection(cls, projection:dict, values:dict[str, list[str] | dict | bool | None])->dict:
        """Validates and if necessary generates projection"""

        def _to_projection(projection:dict, projection_args:list[str]|dict, include:bool)->None:
            """
            Inserts fields in include or exlude arguments inside a projection
            Ex:
                >>> _to_projection({}, projection_args=["abc", "xyz"], include=True)
                {
                    "abc":True,
                    "xyz":True
                }

            Arguments
            ------------------
                - projection_args, list[str]|dict : fields to include or exclude
                - include, bool : whether the fields are to be included or excluded
            """


            if isinstance(projection_args, list):
                for field in projection_args:
                    projection[field] = include
            else:
                projection.update(projection_args)

        # Retrieving validated fields
        # -----------------------------
        include = values.get("include")
        exclude = values.get("exclude")
        fields = values.get("fields")


        # Initizaling projection if not provided
        # --------------------------------------
        if not projection:

            # Case #1 : fields is provided
            # ------------------------------
            if fields:
                # validates_fields ensures that include and exclude are either None or booleans when fields is provided
                # None or boolean_value = boolean_value
                # valdiates_booleans ensures that include or exclude are not both, booleans at the same time
                _to_projection(projection, fields,  include or exclude)

            # Case #2 : fields is not provided
            # -------------------------------
            else:
                if include is not None:
                    _to_projection(projection, include, True)

                if exclude is not None:
                    _to_projection(projection, exclude, False)

        # TODO : Validate final projection <VM, 23/10/2022>
        if not projection:
            raise ValueError(f"Invalid combination of arguments with include={include}, exclude={exclude} and fields={fields}.")

        return projection


    @property
    def statement(self)->dict[str, dict]:
        """Generates statement from other attributes"""

        return self.resolve({"$project":self.projection})
