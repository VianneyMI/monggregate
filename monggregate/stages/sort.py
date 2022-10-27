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

Since the _id field is always guaranteed to contain exclusively unique values,
the returned sort order will always be the same across multiple executions of the same sort.

"""

from pydantic import validator
from monggregate.stages.stage import Stage
from monggregate.utils import to_unique_list

SortArgs = str | list[str] | set[str]

class Sort(Stage):
    """
    Creates a sort statement for an aggregation pipeline sort stage.

    Attributes:
    -----------------------
        - statement, dict : the statement generated after instantiation
        - query, dict : fields-sort order mapping. 1 for ascending order, -1 for descending order. Defaults to {}
                        if not provided, the query will be built from ascending and descending parameters.

        - ascending, set[str] | dict | None : fields to sort on ascending order on
        - descending, set[str] | dict | None : fields to sort on descending order on

    NOTE : When trying to sort on several fields and opposite orders use query rather than using ascending and descending simunateously.

    WARNING : If using the ascending and descending parameters at the same time, the generated query will have the following form:

        >>> query = {
            "ascending_field1" : 1,
            ...
            "ascending_fieldN" : 1,
            "descending_field1" : -1,
            ...
            "descending_fieldN" : -1
        }

    """



    ascending  : list[str] | dict | bool | None = True
    descending : list[str] | dict | bool | None
    by : list[str] | None
    query : dict = {}

    # NOTE : The below are validators are very close to what is used for project => CONSIDER factorizing <VM, 27/10/2022>
    @validator("ascending", "descending", pre=True, always=True)
    @classmethod
    def parse_ascending_descending(cls, value:SortArgs|dict|bool|None)->list[str]|dict|bool|None:
        """Parses ascending and descending"""

        return to_unique_list(value)

    @validator("descending")
    @classmethod
    def validates_boolens(cls, descending:SortArgs|dict|bool|None, values:dict)->list[str]|bool|None:
        """Validates combination of ascending and descending"""

        ascending = values.get("ascending")
        if isinstance(descending, bool) and isinstance(ascending, bool):
            raise ValueError("Cannot use both ascending and descending as booleans at the same time")

        return descending


    @validator("by", pre=True)
    @classmethod
    def validates_by(cls, value:SortArgs|None, values:dict)->list[str]|None:
        """Validates by"""

        ascending = values.get("ascending")
        descending = values.get("descending")

        if value and not (isinstance(ascending, bool) or isinstance(descending, bool)):
            raise ValueError("Either ascending or descending must be set and be a boolean when using fields")

        return to_unique_list(value)


    @validator("query", pre=True, always=True)
    @classmethod
    def generates_query(cls, query:dict, values:dict)->dict:
        """Generates query if not provided"""

        def _to_query(query:dict, sort_args:list[str]|dict, direction:bool)->None:
            """
            Inserts fields in ascending and descending arguments inside a query
            Ex:
                >>> _to_query({}, sort_args=["abc", "xyz"], direction=True)
                {
                    "abc":1,
                    "xyz":-1
                }

            """

            _sort_order_map = {
                True:1, # ascending
                False:-1 # descending
            }

            if isinstance(sort_args, list):
                    for field in sort_args:
                        query[field] = _sort_order_map[direction]
            else:
                query.update(sort_args)


            # Retrieving validated fields
        # -----------------------------
        ascending = values.get("ascending")
        descending = values.get("descending")
        by = values.get("by")


        # Initizaling projection if not provided
        # --------------------------------------
        if not query:

            # Case #1 : By is provided
            # ------------------------------
            if by:
                # validates_by ensures that ascending and descending are either None or booleans when by is provided
                # None or boolean_value = boolean_value
                # valdiates_booleans ensures that ascending or descending are not both, booleans at the same time
                _to_query(query, by,  ascending or descending)

            # Case #2 : by is not provided
            # -------------------------------
            else:
                if ascending is not None:
                    _to_query(query, ascending, True)

                if descending is not None:
                    _to_query(query, descending, False)

        # TODO : Validate final query <VM, 23/10/2022>

        return query

    @property
    def statement(self)->dict[str, dict]:
        """Generates statement from other attributes"""

        return  {"$sort":self.query}
