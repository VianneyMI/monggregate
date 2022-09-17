"""
Module definining an interface to MongoDB $sort stage operation in aggrgation pipeline

"""

from pydantic import root_validator
from app.stages.stage import Stage

class Sort(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    query : dict ={} #| None
    ascending  : set[str] | dict | None # TODO : Allow str and list[str] also
    descending : set[str] | dict | None # TODO : Allow str and list[str] also

    @root_validator(pre=True)
    @classmethod
    def generate_statement(cls, values:dict)->dict[str, dict]:
        """Generates statelent from other attributes"""

        # NOTE : Unlike in the case of the projection, the order of the fields matter here <VM, 17/09/2022>
        # Be providing the fields in two different keys, the order might be broken.
        # So it is prefer to provide the query directly

        def _parse_ascending_descending(ascending_or_descending:set[str]|dict|None, direction:bool)->tuple[dict, bool]:
            """Parses include and exclude arguments"""

            query = {}

            _sort_order_map = {
                True:1, # ascending
                False:-1 # descending
            }

            is_valid = False

            if ascending_or_descending and len(ascending_or_descending)>0:
                is_valid = True

                if isinstance(ascending_or_descending, set):
                    for field in ascending_or_descending:
                        query[field] = _sort_order_map[direction]
                else:
                    query.update(ascending_or_descending)


            return query, is_valid

        query = values.get("query")
        ascending = values.get("ascending")
        descending = values.get("descending")

        if not (query or ascending or descending):
            raise TypeError("At least one of (query, ascending, descending) is required")

        if not query:
            ascending_query, is_ascending_valid = _parse_ascending_descending(ascending, True)
            descending_query, is_descending_valid = _parse_ascending_descending(descending, False)

            query = ascending_query | descending_query
            is_valid = is_ascending_valid or is_descending_valid

            if not is_valid:
                raise ValueError("At least one of (ascending, exclude) must be valid when query is not provided")


        values["statement"] = {"$sort":query}

        return values
