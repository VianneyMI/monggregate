"""
Module defining an interface to MongoDB `$lookup` stage operation in aggregation pipeline.
"""

from monggregate.base import pyd
from monggregate.stages.stage import Stage
from monggregate.utils import StrEnum

class LookupTypeEnum(StrEnum):
    """Enumeration of possible types of lookups"""

    SIMPLE = "simple"
    UNCORRELATED = "uncorrelated"
    CORRELATED = "correlated"

class Lookup(Stage):
    """
    Abstraction for MongoDB `$lookup` statement that performs a left outer 
    join to a collection in the same database to filter in documents from 
    the "joined" collection for processing.

    Parameters
    ----------
    right : str
        Foreign collection.
    from : str
        Alias for `right`.
    left_on : str | None
        Field of the current collection to join on.
    local_field : str | None
        Alias for `left_on`. 
    right_on : str | None
        Field of the foreign collection to join on.
    foreign_field : str | None
        Alias for `right_on`
    let : dict | None
        Variables to be used in the inner pipeline.
    pipeline : list[dict] | None
        Pipeline to run on the foreign collection.
    name : str
        Name of the field containing the matches from the foreign collection.
    as : str
        Alias for `name`.

    NOTE (pipeline and let attributes) : To reference variables in pipeline stages, use the `$$<variable>` syntax.

    The let variables can be accessed by the stages in the pipeline, including additional `$lookup`
    stages nested in the pipeline.

    * A `$match` stage requires the use of an `$expr` operator to access the variables.
        The `$expr` operator allows the use of aggregation expressions inside of the `$match` syntax.

    Starting in MongoDB 5.0, the `$eq`, `$lt`, `$lte`, `$gt`, and `$gte` comparison operators placed in an
    $expr operator can use an index on the from collection referenced in a `$lookup` stage. Limitations:

    * Multikey indexes are not used.

    * Indexes are not used for comparisons where the operand is an array or the operand type is undefined.

    * Indexes are not used for comparisons with more than one field path operand.

    * Other (non-$match) stages in the pipeline do not require an
        `$expr` operator to access the variables.


    Online MongoDB documentation
    ----------------------------
    Performs a left outer join to a collection in the same database to 
    filter in documents from the "joined" collection for processing. The 
    lookup stage adds a new array field to each input document. The new 
    array field contains the matching documents from the "joined" 
    collection. The lookup stage passes these reshaped documents to the next stage.

    Starting in MongoDB 5.1, `$lookup` works across sharded collections.

    To combine elements from two different collections, use the `$unionWith` pipeline stage.

    [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/)
    """

    right : str | None = pyd.Field(None, alias = "from")
    on : str | None #  shortcut for when left_on is the same than right_on
    left_on : str | None = pyd.Field(None,alias = "local_field")
    right_on : str | None = pyd.Field(None, alias = "foreign_field")
    name : str = pyd.Field(...,alias = "as") # | None

    # Subquery fields
    # ---------------------
    let : dict | None # the let variables can be accessed by the stages in the pipeline including additional $lookup stages
                      # nested in
    pipeline : list[dict] | None

    type_ : LookupTypeEnum = pyd.Field("simple", exclude=True)
        # internal variable to know the type of join (simple, correlated, uncorrelated)

    @pyd.validator("left_on", "right_on", pre=True, always=True)
    @classmethod
    def on_alias(cls, value:str, values:dict[str, str])->str:
        """Automatically fills left_on and right_on attributes when on is provided"""

        on = values.get("on") # pylint: disable=invalid-name
        if on:
            value = on

        return value


    @pyd.validator("type_", pre=True, always=True)
    @classmethod
    def set_type(cls, value:str, values:dict)->str:
        """Set types dynamically"""

        
        if value:
            pass
            # TODO : Raise a warning if passed
            # and an error is passed and computed values
            # do not match

        # Retrieve previously validated values
        right = values.get("right")
        left_on = values.get("left_on")
        right_on = values.get("right_on")
        let = values.get("let")
        pipeline = values.get("pipeline")

        # Check combination of arguments
        if right and left_on and right_on\
            and not (let or pipeline):

            type_ = "simple"


        elif let and left_on and right_on\
            and pipeline is not None:

            type_ = "correlated"

        elif not let and pipeline is not None:
                        # in a subquery to select all on the foreign collection
                        # pipeline can be an empty list which is falsy
            type_ =  "uncorrelated"


        else:
            # TODO : Inprove this error message
            # Either maybe just print received arguments
            # Or even better parse received arguments and give reason
            # that is either missing argument or superflous argument <VM, 16/04/2023>
            raise TypeError("Incompatible combination of arguments")

        return type_

    @property
    def statement(self)->dict:
        """Generates statement from attributes"""


        # Generate statement:
        # -----------------------------------------------
        if self.type_ == "simple":
            statement = {
                "$lookup":{
                    "from":self.right,
                    "localField":self.left_on,
                    "foreignField":self.right_on,
                    "as":self.name
                }
            }
        elif self.type_ == "uncorrelated":
            statement = {
                "$lookup":{
                    "from":self.right,
                    "let":self.let,
                    "pipeline":self.pipeline,
                    "as":self.name
                }
            }
        else: # should be correlated case
            statement = {
                "$lookup":{
                    "from":self.right,
                    "localField":self.right_on,
                    "foreignField":self.right_on,
                    "let":self.let,
                    "pipeline":self.pipeline,
                    "as":self.name
                }
            }

        return self.resolve(statement)
