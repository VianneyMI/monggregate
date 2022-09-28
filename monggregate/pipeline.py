"""Pipeline Module"""

from typing import Any
from pymongo.database import Database
from pydantic import BaseModel, BaseConfig
from monggregate.stages import (
    Stage,
    BucketAuto,
    Bucket,
    Count,
    Group,
    Limit,
    Lookup,
    Match,
    Out,
    Project,
    ReplaceRoot,
    Sample,
    Set,
    Skip,
    SortByCount,
    Sort,
    Unwind
)
from monggregate.utils import StrEnum


class OnCallEnum(StrEnum):
    """
    Possible behaviors on pipeline call

        * RUN => the pipeline will execute itself and query the database

        * EXPORT => the pipeline will generate a list of statements that will need
                    to be run externally

    """

    RUN = "run"
    EXPORT = "export"


class Pipeline(BaseModel): # pylint: disable=too-many-public-methods
    """
    MongoDB aggregation pipeline abstraction

    Attributes
    -----------------------
        - collection, str : reference collection for the pipeline.
                            This is the collection where the aggregation will be done.
                            However some stages in the pipeline might work with additional
                            collections (e.g. lookup stage)

        - stages, list[Stage] : the list of Stages that the pipeline is made of.
                                Similarly to the pipeline itself. This package constructs
                                abstraction for MongoDB aggregation framework pipeline stages.

        - on_call, OnCallEnum : pipeline instances are callable. This defines the behavior of the instance
                                when called. See OnCallEnum above. Defaults to export

        - -db, Database : pymongo database instance. Can be optionally provided to make a pipeline instance self sufficient

    Usage
    -----------------------

    You can instantiate a pipeline instance as follow:

        >>> pipeline = Pipeline(collection="listingsAndReviews") # collection is the only mandatory attribute
                                                                # example using MongoDB AirBnB demo dataset : https://www.mongodb.com/docs/atlas/sample-data/sample-airbnb/#std-label-sample-airbnb
    and then add stages to the pipeline by calling its wrapper stages method as shown below:

        >>> pipeline.match(
            query = { "room_type": "Entire home/apt"}
        ).sort_by_count(
            by =  "bed_type"
        )

    and then use this pipeline in your own code:

        >>> db["listingsAndReviews"].aggregate(pipeline=pipeline()) # pipeline() here is actually equivalent to  pipeline.export()

    Alternatively, your pipeline can be self sufficient and executes itself directly using the following approach:

        >>> pipeline = Pipeline(
            _db=db,  # TODO : Update this when adding the uri parameter
            collection="listingsAndReviews",
            on_call="run"
        )

        >>> pipeline.match(
            query = { "room_type": "Entire home/apt"}
        ).sort_by_count(
            by =  "bed_type"
        )

        >>> pipeline() # pipeline() there is actually equivalent to  pipeline.run()


    """

    _db : Database | None # necessary to execute the pipeline
                        # TODO : allow to pass a URI and instantiates a database connection directly here
    on_call : OnCallEnum = OnCallEnum.EXPORT
    collection : str
    stages : list[Stage] = []

    class Config(BaseConfig):
        """Configuration Class for Pipeline"""
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


    # ------------------------------------------------
    # Pipeline Internal Methods
    #-------------------------------------------------

    def __call__(self)->list[dict]:
        """Makes a pipeline instance callable and executes the entire pipeline when called"""

        _on_call_map = {
            OnCallEnum.EXPORT:self.export,
            OnCallEnum.RUN:self.run
        }

        return _on_call_map[self.on_call]()


    def run(self)->list[dict]:
        """Executes the entire pipeline"""

        stages = self.export()
        if self._db is not None:
            array = list(self._db[self.collection].aggregate(pipeline=stages))
        else:
            raise AttributeError("run is not available when no database is provided")

        return array


    def export(self)->list[dict]:
        """
        Exports current pipeline to pymongo format.

            >>> pipeline = Pipeline().match(...).project(...).limit(...).export()
            >>> db.examples.aggregate(pipeline=pipeline)

        """

        stages = []
        for stage in self.stages:
            stages.append(stage())

        return stages


    def to_statements(self)->list[dict]:
        """Alias for export method"""

        return self.export()


    #-----------------------------------------------------------
    # Stages
    #-----------------------------------------------------------
    # The below methods wrap the constructors of the classes of the same name

    def add_fields(self, **kwargs:Any)->"Pipeline":
        """
        Adds an add_fields stage to the current pipeline.

        Arguments:
        ---------------------------------
            - statement, dict :
            - document, dict : new fields to be added

        """

        self.stages.append(
            Set(**kwargs)
        )
        return self

    def bucket(self, **kwargs:Any)->"Pipeline":
        """
        Adds a bucket stage to the current pipeline.

        Arguments:
        ---------------------------------
            by : str|list[str]|set[str], field or fields to group the documents
                                        unless a default is provided, each input document
                                        must resolve the groupBy field path or expression
                                        to a value that falls within one of the ranges specified
                                        by the boundaries
            boundaries : list, an array of values that specify the boundaries for each bucket.
                            Each adjacent pair of values acts as the inclusive lower boundary
                            and the exclusive upper boundary for the bucket.
                            NOTE : You must specify at least two boundaries.
            default : Any, Optional. A literal that specifies the _id (group name) of an additional
                                    bucket that contains all documents whoe groupBy expression result
                                    does not fall into a bucket specified by the boundaries

                                    If unspecified, each input document must resolve groupBy
                                    expression to a value within one of the bucket ranges.

                                    The default value must be less than the lowest boundary or greather
                                    than or equal to the highest boundary value

                                    The default value can be of a different type than the entries in boundaries
            output : dict | None, A document that specifies the fields to include in the output documents in addition to
                                the _id field. To specify the field to include you must use accumulator expressions
                                    >>> {"outputField1" : {"accumulator":"expression1}}
                                        ....
                                        {"outputField2" : {"accumulator":"expression2}}
                                If you do not specify an output document, the operation returns a count field containing
                                the number of documents in each bucket.

                                If you specify and output document, only the fields specified in the document are returned; i.e.
                                the count field is not returned unless it is explicitly included in the output document


        """

        self.stages.append(
            Bucket(**kwargs)
        )
        return self

    def bucket_auto(self, **kwargs:Any)->"Pipeline":
        """
        Adds a bucket_auto stage to the current pipeline

        Arguments:
        ---------------------------------
        by : str|list[str]|set[str], An expression to group documents. To specify a field path
                                     prefix the field name with a dollar sign $ and enclose it in quotes.
        buckets : int, number of buckets desired
        output : dict, A document that specifieds the fields to include in the oupput documents in addition
                       to the _id field. To specify the field to include, you must use accumulator expressions.

                       The defaut count field is not included in the output document when output is specified. Explicitly specify the count expression
                       as part of the output document to include it:

                       >>> {
                                <outputfield1>: { <accumulator>: <expression1> },
                                ...
                                count: { $sum: 1 }
                           }
        granularity : str | None, A string that specifies the preferred number series to use to ensure that the calculated
                                  boundary edges end on preferred round numbers of their powers of 10.

                                  Available only if the all groupBy values are numeric and none of them are NaN.
                                  https://en.wikipedia.org/wiki/Preferred_number
                                  TODO : Need to understand this <VM, 18/09/2022>

        """

        self.stages.append(
            BucketAuto(**kwargs)
        )
        return self


    def count(self, **kwargs:Any)->"Pipeline":
        """
        Adds a count stage to the current pipeline

        Arguments
        -------------------------------

            - name, str : name of the output field which the count as its value.
                        Must be a non-empty string,
                        NOTE : Must not start with $ and must not contain the
                                . character.

        """

        self.stages.append(
                Count(**kwargs)
            )
        return self

    def explode(self, **kwargs:Any)->"Pipeline":
        """
        Adds a unwind stage to the current pipeline.

        Arguments:
        ---------------------------------

            - path_to_array (path), str : path to an array field
            - include_array_index, str : name of a new field to hold the array index of the element
                                        NOTE : The name cannot start with a dollar sign
            - always (preserve_null_and_empty_index), bool : whether to output documents for input documents where the path does not resolve to a valid array. Defaults to False

        """

        self.stages.append(
                Unwind(**kwargs)
            )
        return self

    def group(self, **kwargs:Any)->"Pipeline":
        """
        Adds a group stage to the current pipeline.

        Arguments:
        ------------------------
            - by / _id (offcial MongoDB name represented by a pydantic alias), str | list[str] | set[str] : field or group of fields to group on
            - query, dict | None : Computed aggregated values (per group)

        """

        self.stages.append(
                Group(**kwargs)
            )
        return self

    def limit(self, **kwargs:Any)->"Pipeline":
        """
        Adds a limit stage to the current pipeline.

        Arguments:
        ---------------------------------
            - value, int : the actual limit to apply.
                           limits the number of documents returned by the stage to
                           the provided value.

        """

        self.stages.append(
                Limit(**kwargs)
            )
        return self

    def lookup(self, **kwargs:Any)->"Pipeline":
        """
        Adds a lookup stage to the current pipeline.

        Arguments:
        ----------------------------
            - right / from (official MongoDB name), str : foreign collection
            - left_on / local_field (official MongoDB name)), str | None : field of the current collection to join on
            - right_on / foreign_field (official MongoDB name), str | None : field of the foreign collection to join on
            - let, dict | None : variables to be used in the inner pipeline
            - pipeline, list[dict] | None : pipeline to run on the foreign collection.
            - as, str : name of the field containing the matches from the foreign collection

        """

        self.stages.append(
            Lookup(**kwargs)
        )
        return self

    def match(self, **kwargs:Any)->"Pipeline":
        """
        Adds a match stage to the current pipeline.

        Arguments:
        -------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - query, dict : the query use to filter the documents


        """

        self.stages.append(
                Match(**kwargs)
            )
        return self

    def out(self, **kwargs:Any)->"Pipeline":
        """
        Adds an out stage to the current pipeline.

        Arguments:
        ---------------------------
            - db, str|None : name of the db to output the collection. Defaults to current collection.
            - collectin, str : name of the output collection


        """

    def project(self, **kwargs:Any)->"Pipeline":
        """
        Adds a project stage to the current pipeline.

        Arguments:
        ---------------------------
            - projection, dict | None : projection to be applied
            - include, str | list[str] | set[str] | dict | None : fields to be kept
            - exclude, str | list[str] | set[str] | dict | None : fields to be excluded


        """

        self.stages.append(
                Project(**kwargs)
            )
        return self

    def replace_root(self, **kwargs:Any)->"Pipeline":
        """
        Adds a replace_root stage to the current pipeline.

        Arguments:
        -------------------------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - path_to_new_root, str : the path to the embedded document to be promoted
            - document, dict : documents being created and to be set as the new root (Not implemented yet)


        """

        self.stages.append(
                ReplaceRoot(**kwargs)
            )
        return self

    def replace_with(self, **kwargs:Any)->"Pipeline":
        """
        Adds a replace_with stage to the current pipeline.

        Arguments:
        -------------------------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - path_to_new_root, str : the path to the embedded document to be promoted
            - document, dict : documents being created and to be set as the new root (Not implemented yet)

        """

        self.stages.append(
                ReplaceRoot(**kwargs)
            )
        return self

    def sample(self, **kwargs:Any)->"Pipeline":
        """
        Adds a sample stage to the current pipeline.

        Arguments:
        -----------------------
            - statement, dict : the statement generated after instantiation
            - value, int : positive integer representing the number of documents to be randomly picked. Defaults to 10.


        """

        self.stages.append(
                Sample(**kwargs)
            )
        return self

    def set(self, **kwargs:Any)->"Pipeline":
        """
        Adds a set stage to the current pipeline.

        Arguments:
        ---------------------------------
            - statement, dict :
            - document, dict : new fields to be added

        """

        self.stages.append(
                Set(**kwargs)
            )
        return self

    def skip(self, **kwargs:Any)->"Pipeline":
        """
        Adds a skip stage to the current pipeline.

        Arguments:
        -----------------------
            - statement, dict : the statement generated after instantiation
            - value, int : positive integer representing the number of documents to be skipped.

        """

        self.stages.append(
                Skip(**kwargs)
            )
        return self

    def sort(self, **kwargs:Any)->"Pipeline":
        """
        Adds a sort stage to the current pipeline.

        Arguments:
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

        self.stages.append(
                Sort(**kwargs)
            )
        return self

    def sort_by_count(self, **kwargs:Any)->"Pipeline":
        """
        Adds a sort_by_count stage to the current pipeline.


        Arguments:
        -------------------------
            - _statement, dict : the statement generated during the validation process
            - by, str : the key to group, sort and count on


        """

        self.stages.append(
                SortByCount(**kwargs)
            )
        return self

    def unwind(self, **kwargs:Any)->"Pipeline":
        """
        Adds a unwind stage to the current pipeline.

        Arguments:
        ---------------------------------

            - path_to_array (path), str : path to an array field
            - include_array_index, str : name of a new field to hold the array index of the element
                                    NOTE : The name cannot start with a dollar sign
            - always (preserve_null_and_empty_index), bool : whether to output documents for input documents where the path does not resolve to a valid array. Defaults to False

        """

        self.stages.append(
                Unwind(**kwargs)
            )
        return self




if __name__ == "__main__":
    pipeline = Pipeline(stages=[])
    pipeline()