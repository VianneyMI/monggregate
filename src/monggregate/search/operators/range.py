"""
Module defining an interface to MongoDB Atlas Search range operator 

Online MongoDB documentation:
----------------------------------------------
Last updated (in this package) : 26/04/2023
Source : https://www.mongodb.com/docs/atlas/atlas-search/range/

# Definition
# --------------------------------------------

The range operator supports querying and scoring numeric and date values. 
This operator can be used to perform a search over:

    *  Number fields of BSON int32, int64, and double data types.

    * Date fields of BSON date data type in ISODate format.

You can use the range operator to find results that are within a given numeric or date range.

# Syntax
# ----------------------------------------------
range has the following syntax:

    >>> {
            "$search": {
            "index": <index name>, // optional, defaults to "default"
            "range": {
                "path": "<field-to-search>",
                "gt | gte": <value-to-search>,
                "lt | lte": <value-to-search>,
                "score": <score-options>
            }
            }
        }

# Options
# ---------------------------------------------

Field           Type                    Description                             Necessity

gt or gte       date or number          Find values greater (>) than            no
                                        or greater than or equal to (>=)    
                                        the given value.
                                        * For number fields, the value
                                          can be an int32, int64, or double.
                                          data type.
                                        * For date fields, the value must an
                                          ISODate formatted date.

lt or lte       date or number          Find values less (<) than               no
                                        or less than or equal to (<=)
                                        the given value.
                                        * For number fields, the value
                                          can be an int32, int64, or double.
                                        * For date fields, the value must an
                                          ISODate formatted date.

path            string                  Indexed field or fields.                 yes

score           object                  Modify the score assigned to matching    no
                                        search results. Options are:
                                        * boost: multiply the score by the
                                                 given positive number.
                                        *constant: replace the score with the
                                                   given number.                       
"""


from datetime import datetime
from monggregate.base import pyd
from monggregate.search.operators.operator import SearchOperator

class Range(SearchOperator, smart_union=True):
    """
    Creates a range operator for MongoDB Atlas Search query.

    Description
    --------------------
    You can use the range operator to find results that are within a given numeric or date range.
    

    Attributes
    --------------------
        - gt/gte, numeric or date : Upper bound (exclusive/inclusive) of the range 
        - lt/lte, numeric or date : Lower bound (exclusive/inclusive) of the range
        - path, str | list[str] : Indexed field or fields to search.
        - score, dict : Scoring options

    """

    path : str | list[str]
    gt : int | float | datetime | None = None
    lt : int | float | datetime | None = None
    gte : int | float | datetime | None = None
    lte : int | float | datetime | None = None
    score : dict|None

    @pyd.validator("gte", pre=True, always=True)
    def at_least_one_lower(cls, value, values):
        if value is None and values.get("gt") is None:
            raise ValueError("at least one of gte or gt must be specified")
        return value
    
    @pyd.validator("lte", pre=True, always=True)
    def at_least_one_upper(cls, value, values):
        if value is None and values.get("lt") is None:
            raise ValueError("at least one of lte or lt must be specified")
        return value


    @property
    def statement(self) -> dict:
            
            params = {
                "path": self.path,
                "score": self.score
            }
            
            if self.gt is not None:
                params["gt"] = self.gt
            else:
                params["gte"] = self.gte

            if self.lt is not None:
                params["lt"] = self.lt
            else:
                params["lte"] = self.lte

            return self.resolve({"range":params})
    