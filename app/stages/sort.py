"""
Module definining an interface to MongoDB $sort stage operation in aggrgation pipeline

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------

Last Updated (in this package) : 21/09/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort

Definition
--------------------------------------------

Sorts all input documents and returns them to the pipeline in sorted order.

The $sort stage has the following prototype form:

    >>> { $sort: { <field1>: <sort order>, <field2>: <sort order> ... } }

$sort takes a document that specifies the field(s) to sort by and the respective sort order. <sort order> can have one of the following values:

| Value             | Descriotion           |
|-------------------|-----------------------|
| 1                 | Sort ascending        |
|-------------------|-----------------------|
| -1                | Sort descending       |
|-------------------|-----------------------|
|{                  | Sort by the computed  |
| $meta:"textScore" | textScore metadata in |
|}                  | descending order      |

If sorting on multiple fields, sort order is evaluated from left to right.
For example, in the form above, documents are first sorted by <field1>. Then documents with the same <field1> values are further sorted by <field2>.


Behavior
----------------------------------------

Limits

You can sort on a maximum of 32 keys.

Sort consistency

MongoDB does not store documents in a collection in a particular order. When sorting on a field which contains duplicate values, documents containing those values may be returned in any order.

If consistent sort order is desired, include at least one field in your sort that contains unique values. The easiest way to guarantee this is to include the _id field in your sort query.

Consider the following restaurant collection:

    >>> db.restaurants.insertMany([
            { "_id" : 1, "name" : "Central Park Cafe", "borough" : "Manhattan"},
            { "_id" : 2, "name" : "Rock A Feller Bar and Grill", "borough" : "Queens"},
            { "_id" : 3, "name" : "Empire State Pub", "borough" : "Brooklyn"},
            { "_id" : 4, "name" : "Stan's Pizzaria", "borough" : "Manhattan"},
            { "_id" : 5, "name" : "Jane's Deli", "borough" : "Brooklyn"},
        ]);

The following command uses the $sort stage to sort on the borough field:

    >>> db.restaurants.aggregate(
            [
                { $sort : { borough : 1 } }
            ]
        )

In this example, sort order may be inconsistent, since the borough field contains duplicate values for both Manhattan and Brooklyn.
Documents are returned in alphabetical order by borough, but the order of those documents with duplicate values for borough might not the be the same across multiple executions of the same sort.
For example, here are the results from two different executions of the above command:

    >>> { "_id" : 3, "name" : "Empire State Pub", "borough" : "Brooklyn" }
        { "_id" : 5, "name" : "Jane's Deli", "borough" : "Brooklyn" }
        { "_id" : 1, "name" : "Central Park Cafe", "borough" : "Manhattan" }
        { "_id" : 4, "name" : "Stan's Pizzaria", "borough" : "Manhattan" }
        { "_id" : 2, "name" : "Rock A Feller Bar and Grill", "borough" : "Queens" }
        { "_id" : 5, "name" : "Jane's Deli", "borough" : "Brooklyn" }
        { "_id" : 3, "name" : "Empire State Pub", "borough" : "Brooklyn" }
        { "_id" : 4, "name" : "Stan's Pizzaria", "borough" : "Manhattan" }
        { "_id" : 1, "name" : "Central Park Cafe", "borough" : "Manhattan" }
        { "_id" : 2, "name" : "Rock A Feller Bar and Grill", "borough" : "Queens" }

While the values for borough are still sorted in alphabetical order, the order of the documents containing duplicate values for borough (i.e. Manhattan and Brooklyn) is not the same.

To achieve a consistent sort, add a field which contains exclusively unique values to the sort. The following command uses the
$sort stage to sort on both the borough field and the _id field:

    >>> db.restaurants.aggregate(
            [
                { $sort : { borough : 1, _id: 1 } }
            ]
        )

Since the _id field is always guaranteed to contain exclusively unique values, the returned sort order will always be the same across multiple executions of the same sort.

"""

from pydantic import root_validator
from app.stages.stage import Stage

class Sort(Stage):
    """
    TBD

    """

    statement : dict # TODO : Fine tune type <VM, 16/09/2022> Ex : dict[str, str|dict]
    query : dict ={} #| None
    ascending  : set[str] | dict | None # TODO : Allow str and list[str] also and bool (when by is passed)
    descending : set[str] | dict | None # TODO : Allow str and list[str] also and bool (when by is passed)

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
