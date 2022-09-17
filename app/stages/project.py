"""
Module defining an interface to MongoDB $project stage operation in aggregation pipeline

Online MongoDB documentation:
---------------------------------------------------------------------------------------
Last Updated :
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project


"""

# NOTE : This is a first prototype, there are so much that can be done by $project that this will be completed
# after further reading the doc and copying here and
# after having prototype more stages

# NOTE : Would be nice and useful to have something keywords arguments based to generate the projection <VM, 16/09/2022>
# (on top[on the side] of the below)
from pydantic import root_validator

from app.stages.stage import Stage

class Project(Stage):
    """"

    """

    statement : dict
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

            projection = include_projection | exclude_projection
            is_valid = is_include_valid or is_exclude_valid

            if not is_valid:
                raise ValueError("At least one of (include, exclude) must be valid when projection is not provided")


        values["statement"] = {"$project":projection}

        return values
