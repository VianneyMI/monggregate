"""Pipeline Module"""

from typing import Any, Literal
from warnings import warn
from pymongo.database import Database
from monggregate.base import BaseModel
from monggregate.stages import (
    Stage,
    BucketAuto,
    GranularityEnum,
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
    Search,
    SearchMeta,
    Set,
    Skip,
    SortByCount,
    Sort,
    UnionWith,
    Unwind,
    Unset
)
from monggregate.stages.search import OperatorLiteral
from monggregate.search.operators.compound import Compound
from monggregate.operators import MergeObjects
from monggregate.dollar import ROOT
from monggregate.utils import StrEnum



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
            _db=db,
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

    stages : list[Stage] = []
    _db : Database | None = None# necessary to execute the pipeline
    collection : str | None =None
    

    @property
    def statement(self)->list[dict]:
        """Returns the pipeline statement"""

        return [stage.statement for stage in self.stages]




    # ------------------------------------------------
    # Pipeline Internal Methods
    #-------------------------------------------------
    def __call__(self)->list[dict]:
        """Makes a pipeline instance callable and executes the entire pipeline when called"""
   
        return self.run()

    
    def run(self)->list[dict]:
        """Executes the entire pipeline"""

        if self._db is None:
            raise ValueError("db is not defined. Please indicate which database to run the pipeline on")

        if not self.collection:
            raise ValueError("collection is not defined. Please indicate which collection to run the pipeline on")

        stages = self.export()
        array = list(self._db[self.collection].aggregate(pipeline=stages))
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

    # --------------------------------------------------
    # Pipeline List Methods
    #---------------------------------------------------
    def __add__(self, other:"Pipeline")->"Pipeline":
        """Concatenates two pipelines together"""
        if not isinstance(other, Pipeline):
            raise TypeError(f"unsupported operand type(s) for +: 'Pipeline' and '{type(other)}'")
        
        return Pipeline(
            _db=self._db,
            collection=self.collection, 
            stages=self.stages + other.stages
            )
    
    def __getitem__(self, index:int)->Stage:
        """Returns a stage from the pipeline"""
        # https://realpython.com/inherit-python-list/
        return self.stages[index]

    def __setitem__(self, index:int, stage:Stage)->None:
        """Sets a stage in the pipeline"""
        self.stages[index] = stage

    def __delitem__(self, index:int)->None:
        """Deletes a stage from the pipeline"""
        del self.stages[index]

    def __len__(self)->int:
        """Returns the length of the pipeline"""
        return len(self.stages)
    
    def append(self, stage:Stage)->None:
        """Appends a stage to the pipeline"""
        self.stages.append(stage)

    def insert(self, index:int, stage:Stage)->None:
        """Inserts a stage in the pipeline"""
        self.stages.insert(index, stage)

    def extend(self, stages:list[Stage])->None:
        """Extends the pipeline with a list of stages"""
        self.stages.extend(stages)


    #---------------------------------------------------
    # Stages
    #---------------------------------------------------
    # The below methods wrap the constructors of the classes of the same name

    def add_fields(self, document:dict={}, **kwargs:Any)->"Pipeline":
        """
        Adds an add_fields stage to the current pipeline.

        Arguments:
        ---------------------------------
            - statement, dict :
            - document, dict : new fields to be added

        """

        document = document | kwargs
        self.stages.append(
            Set(document=document)
        )
        return self

    def bucket(self, *, by:Any, boundaries:list, default:Any=None, output:dict|None=None)->"Pipeline":
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
            Bucket(
                by = by,
                boundaries = boundaries,
                default = default,
                output = output
            )
        )
        return self

    def bucket_auto(self, *, by:Any, buckets:int, output:dict=None, granularity:GranularityEnum|None=None)->"Pipeline":
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

        """

        self.stages.append(
            BucketAuto(
                by = by,
                buckets = buckets,
                output = output,
                granularity = granularity
            )
        )
        return self


    def count(self, name:str)->"Pipeline":
        """
        Adds a count stage to the current pipeline

        Arguments
        -------------------------------

            - name, str : name of the output field which the count as its value.
                        Must be a non-empty string,
                        NOTE : Must not start with $ and must not contain the
                                . character and must not be empty

        """

        self.stages.append(
                Count(name=name)
            )
        return self

    def explode(self, path:str, *,  include_array_index:str|None=None, always:bool=False)->"Pipeline":
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
                Unwind(
                    path=path,
                    include_array_index=include_array_index,
                    always=always
                    )
            )
        return self

    def group(self, *,  by:Any|None=None, query:dict={})->"Pipeline":
        """
        Adds a group stage to the current pipeline.

        Arguments:
        ------------------------
            - by,  str | list[str] | set[str] | dict | None : field or group of fields to group by
            - query, dict | None : Computed aggregated values (per group)

        """

        self.stages.append(
                Group(
                    by=by,
                    query=query
                )
            )
        return self

    def limit(self, value:int)->"Pipeline":
        """
        Adds a limit stage to the current pipeline.

        Arguments:
        ---------------------------------
            - value, int : the actual limit to apply.
                           limits the number of documents returned by the stage to
                           the provided value.

        """

        self.stages.append(
                Limit(value=value)
            )
        return self

    def lookup(self, *, \
        name:str,
        right:str|None=None,
        on:str|None=None,
        left_on:str|None=None,
        right_on:str=None)->"Pipeline":
        """
        Adds a lookup stage to the current pipeline.

        Arguments:
        ----------------------------
            - right / from (official MongoDB name), str : foreign collection
            - left_on / local_field (official MongoDB name)), str | None : field of the current collection to join on
            - right_on / foreign_field (official MongoDB name), str | None : field of the foreign collection to join on
            - let, dict | None : variables to be used in the inner pipeline
            - pipeline, list[dict] | None : pipeline to run on the foreign collection.
            - name / as, str : name of the field containing the matches from the foreign collection

            NOTE (pipeline and let attributes) : To reference variables in pipeline stages, use the "$$<variable>" syntax.

            The let variables can be accessed by the stages in the pipeline, including additional $lookup
            stages nested in the pipeline.

            * A $match stage requires the use of an $expr operator to access the variables.
            The $expr operator allows the use of aggregation expressions inside of the $match syntax.

            Starting in MongoDB 5.0, the $eq, $lt, $lte, $gt, and $gte comparison operators placed in an
            $expr operator can use an index on the from collection referenced in a $lookup stage. Limitations:

                * Multikey indexes are not used.

                * Indexes are not used for comparisons where the operand is an array or the operand type is undefined.

                * Indexes are not used for comparisons with more than one field path operand.

            * Other (non-$match) stages in the pipeline do not require an
            $expr operator to access the variables.

        """

        self.stages.append(
            Lookup(
                right = right,
                on = on,
                left_on = left_on,
                right_on = right_on,
                name =name
            )
        )
        return self

    def join(
            self,
            *,
            other:str,
            how:Literal["left", "right", "inner"]="left", # TODO : Implement outer and cross joins <VM, 10/04/2023>
            on:str|None=None,
            left_on:str|None=None,
            right_on:str|None=None  
            )->"Pipeline":
        """
        Adds a combination of stages, that together reproduce SQL joins.
        This is a virtual and unofficial stage. It is not documented on MongoDB aggregation pipeline reference page.
        As such, there is no Join class implementation in this package.

        Arguments:
        -------------------
            - other, str : collection to join
            - how, 'left', 'right', 'inner' : type of join to be performed
                                              'left' preserve the left collection
                                              'right' preserve the right collection
                                              'inner' returns only documents from
                                                      the left collection that match
                                                      documents from the right collection

            - on, str|None=None: key to use to perform the join, 
                                 if the key name is the same in both collections
            - left_on, str|None=None: key to use on the left collection to perform the join.
                                     Must be use with right_on.
            - right_on, str|None=None: key to use on the right collection to perform the join
                                      Must be use with left_on. 
        """

        # NOTE : Currently chose to implement a real SQL join, that is we chose to promote the matches in the local collection, the matches of the foreign collection
        # instead of gathering them in an array as the lone lookup stage does.
        # Could be better to leave this choice to the user and implement both approach using a variable to determine which implementation to take
        warning_message = """ 
        If the two collections contain identical key names, the right collection keys will override the left collection keys.
        In a future version, this will be improved and the common keys will be prefixed by the collection name. 
        """

        warn(warning_message)

        if how == "left":
            self.__left_join(right=other, on=on, left_on=left_on, right_on=right_on)
        elif how == "right":
            self.__right_join(left=other, on=on, left_on=left_on, right_on=right_on)
        elif how == "inner":
            self.__inner_join(right=other, on=on, left_on=left_on, right_on=right_on)

        return self
    
    def __join_common(self, right:str, on:str|None, left_on:str|None, right_on:str|None)->str:
        """Common parts between various join types"""


        _prefix = right.lower()
        join_field = "__" + _prefix + "__"
        self.stages.append(
            Lookup(
                right = right,
                on = on,
                left_on = left_on,
                right_on = right_on,
                name = join_field
            )
        )
        self.stages.append(
            Unwind(path_to_array=join_field)
        )
        self.stages.append(
            ReplaceRoot(
                document=MergeObjects(
                    expression=[ROOT, "$"+join_field]
                ).statement
            )
        )
        self.stages.append(
            Project(exclude=join_field)
        )
        return join_field

    def __left_join(self, right:str, on:str|None, left_on:str|None, right_on:str|None) -> None:
        """Implements SQL left join"""

        self.__join_common(right=right, on=on, left_on=left_on, right_on=right_on)
    
    def __right_join(self, left:str, on:str|None, left_on:str, right_on:str|None) -> None:
        """Implements SQL right join"""
        
        warn("This stage will override the collection attribute of the pipeline with left and may lead to strange behaviors if not anticipated.")
        # TODO : Warns that this will override current pipeline collection by left
        # TODO : Append collection name in foreign collection documents field names to avoid collision and override of field when promoting sub-documents
        # Ex : {"a":1, "b":2, "c":{"a":3, "d":0}} after promoting "c" would become {"a":3, "b":2, "d":0} and we want to prevent this

        right = self.collection
        self.collection = left
        self.__join_common(right=right, on=on, left_on=left_on, right_on=right_on)
        
    def __inner_join(self, right:str, on:str|None, left_on:str|None, right_on:str|None) -> None:
        """Implements SQL inner join"""

        join_field = self.__join_common(right=right, on=on, left_on=left_on, right_on=right_on)
        
        filter_no_match = Match(
            query = {
                join_field : []
            }
        ) # used to filter out documents in the left collection, that has no match in the right collection

        self.stages.insert(-3, filter_no_match)

    def match(self, query:dict={}, **kwargs:Any)->"Pipeline":
        """
        Adds a match stage to the current pipeline.

        Arguments:
        -------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - query, dict : the query use to filter the documents


        """

        query = query | kwargs
        self.stages.append(
                Match(query=query)
            )
        return self

    def out(self, collection:str, *, db:str|None=None)->"Pipeline":
        """
        Adds an out stage to the current pipeline.

        Arguments:
        ---------------------------
            - db, str|None : name of the db to output the collection. Defaults to current collection.
            - collection, str : name of the output collection

        """

        self.stages.append(
            Out(
                collection=collection,
                db = db
            )
        )
        return self

    def project(self, *,\
        include : str|set[str]|list[str]|dict|bool|None = None,
        exclude : str|set[str]|list[str]|dict|bool|None = None,
        fields : str|set[str]|list[str]|None = None,
        projection : dict = {},
        **kwargs:Any)->"Pipeline":
        """
        Adds a project stage to the current pipeline.

        Arguments:
        ---------------------------
            - projection, dict | None : projection to be applied
            - fields, ProjectionArgs | None : fields  to be kept or excluded (depending on include/exclude parameters when those are booleans)
            - include, ProjectionArgs| dict | bool | None : fields to be kept
            - exclude, ProjectionArgs | dict | bool | None : fields to be excluded


        """

        projection = projection | kwargs
        self.stages.append(
                Project(
                    include = include,
                    exclude = exclude,
                    fields = fields,
                    projection = projection
                )
            )
        return self

    def replace_root(self, path:str|None=None, *, document:dict|None=None)->"Pipeline":
        """
        Adds a replace_root stage to the current pipeline.

        Arguments:
        -------------------------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - path_to_new_root, str|None : the path to the embedded document to be promoted
            - document, dict|None : document being created and to be set as the new root or expression


        """

        self.stages.append(
                ReplaceRoot(path=path, document=document)
            )
        return self

    def replace_with(self, path:str|None=None, *,document:dict|None=None)->"Pipeline":
        """
        Adds a replace_with stage to the current pipeline.

        Arguments:
        -------------------------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - path_to_new_root, str|None : the path to the embedded document to be promoted
            - document, dict|None : document being created and to be set as the new root or expression

        """

        self.stages.append(
                ReplaceRoot(path=path, document=document)
            )
        return self

    def sample(self, value:int)->"Pipeline":
        """
        Adds a sample stage to the current pipeline.

        Arguments:
        -----------------------
            - statement, dict : the statement generated after instantiation
            - value, int : positive integer representing the number of documents to be randomly picked. Defaults to 10.


        """

        self.stages.append(
                Sample(value=value)
            )
        return self
    
    def search(
            self,
            path:str|list[str]=None,
            query:str|list[str]=None,
            *,
            operator_name:OperatorLiteral="text",
            index:str="default",
            count:dict|None=None,
            highlight:dict|None=None,
            return_stored_source:bool=False,
            score_details:bool=False,
            **kwargs:Any
    )->"Pipeline":
        """
        Adds a search stage to the current pipeline
        NOTE : if used, search has to be the first stage of the pipeline

        Arguments:
        -------------------------------
            - path, str|list[str]|None : field to search in
            - query, str|list[str]|None : text to search for
            - index, str : name of the index to use for the search. Defaults to defaut
            - count, dict|None : document that specifies the count options for retrieving
                                 a count of the results
            - highlight, dict|None : document that specifies the highlight options for 
                                     displaying search terms in their original context
            - return_stored_source, bool : Indicates whether to use the copy of the documents
                                           in the Atlas Search index (with just a subset of the fields)
                                           or to return the original full document (slower).
                                           Defaults to False.
                                           True => Use the copy
                                           False => Do a lookup and return the original documents.
            - score_details, bool : Indicates whether to retrieve the detailed breakdown of the score for
                                    the documents in the results. Defaults to False.
                                    To view the details, you must use the $meta expression in the 
                                    $project stage.
            - operator_name, str : Name of the operator to search with. Use the compound operator to run a 
                              compound (i.e query with multiple operators).
            - kwargs, Any : Operators specific options.
                            Includes (non-exhaustive):
                            - fuzzy, FuzzyOptions (controls fuzzy matching options)
                            - score, dict (controls scoring options)
                            - value, numeric|bool|date (for filtering)
                            - allow_analyzed_field, bool (controls index scanning)
                            - synonyms
                            - like, dict|list[dict] (allow looking for similar documents)
        """
        
        self.stages.append(
            Search.from_operator(
                operator_name=operator_name,
                path=path,
                query=query,
                index=index,
                count=count,
                highlight=highlight,
                return_stored_source=return_stored_source,
                score_details=score_details,
                **kwargs
            )
        )
        

        return self
    
    def search_compound(self)->"Compound":
        """Adds a compound search stage"""

        self.stages.insert(
            0,
            Search.compound()
        )
        return self.stages[0]

    
    def search_meta(
            self,
            path:str|list[str]=None,
            query:str|list[str]=None,
            *,
            operator_name:OperatorLiteral="text",
            index:str="default",
            count:dict|None=None,
            highlight:dict|None=None,
            return_stored_source:bool=False,
            score_details:bool=False,
            **kwargs:Any
    )->"Pipeline":
        """
        Adds a searchMeta stage to the current pipeline
        NOTE : if used, search has to be the first stage of the pipeline

        Arguments:
        -------------------------------
            - path, str|list[str]|None : field to search in
            - query, str|list[str]|None : text to search for
            - index, str : name of the index to use for the search. Defaults to defaut
            - count, dict|None : document that specifies the count options for retrieving
                                 a count of the results
            - highlight, dict|None : document that specifies the highlight options for 
                                     displaying search terms in their original context
            - return_stored_source, bool : Indicates whether to use the copy of the documents
                                           in the Atlas Search index (with just a subset of the fields)
                                           or to return the original full document (slower).
                                           Defaults to False.
                                           True => Use the copy
                                           False => Do a lookup and return the original documents.
            - score_details, bool : Indicates whether to retrieve the detailed breakdown of the score for
                                    the documents in the results. Defaults to False.
                                    To view the details, you must use the $meta expression in the 
                                    $project stage.
            - operator_name, str : Name of the operator to search with. Use the compound operator to run a 
                              compound (i.e query with multiple operators).
            - kwargs, Any : Operators specific options.
                            Includes (non-exhaustive):
                            - fuzzy, FuzzyOptions (controls fuzzy matching options)
                            - score, dict (controls scoring options)
                            - value, numeric|bool|date (for filtering)
                            - allow_analyzed_field, bool (controls index scanning)
                            - synonyms
                            - like, dict|list[dict] (allow looking for similar documents)
        """
        
        self.stages.append(
            SearchMeta.from_operator(
                operator_name=operator_name,
                path=path,
                query=query,
                index=index,
                count=count,
                highlight=highlight,
                return_stored_source=return_stored_source,
                score_details=score_details,
                **kwargs
            )
        )
        

        return self

    def set(self, document:dict={}, **kwargs:Any)->"Pipeline":
        """
        Adds a set stage to the current pipeline.

        Arguments:
        ---------------------------------
            - statement, dict :
            - document, dict : new fields to be added

        """

        document = document | kwargs
        self.stages.append(
                Set(document=document)
            )
        return self

    def skip(self, value:int)->"Pipeline":
        """
        Adds a skip stage to the current pipeline.

        Arguments:
        -----------------------
            - statement, dict : the statement generated after instantiation
            - value, int : positive integer representing the number of documents to be skipped.

        """

        self.stages.append(
                Skip(value=value)
            )
        return self

    def sort(self, *,\
        descending : str|list[str]|dict|bool|None = None,
        ascending : str|list[str]|dict|bool|None = None,
        by : list[str]|None = None,
        query : dict[str, Literal[1, -1]] = {},
        **kwargs:Any)->"Pipeline":
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

        query = query | kwargs
        self.stages.append(
                Sort(
                    descending = descending,
                    ascending = ascending,
                    by = by,
                    query = query
                )
            )
        return self

    def sort_by_count(self, by:str)->"Pipeline":
        """
        Adds a sort_by_count stage to the current pipeline.


        Arguments:
        -------------------------
            - _statement, dict : the statement generated during the validation process
            - by, str : the key to group, sort and count on


        """

        self.stages.append(
                SortByCount(by=by)
            )
        return self
    
    def union_with(self, collection:str, pipeline:list[dict]|None=None)->"Pipeline":
        """
        Adds a union_with stage to the current pipeline.

        Arguments:
        ---------------------------------
            - collection / coll, str : The collection or view whose pipeline results you wish to include in the result set
            - pipeline, list[dict] | Pipeline | None : An aggregation pipeline to apply to the specified coll.

        """

        self.stages.append(
            UnionWith(collection=collection, pipeline=pipeline)
        )

        return self

    def unwind(self, path:str, include_array_index:str|None=None, always:bool=False)->"Pipeline":
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
                Unwind(
                    path = path,
                    include_array_index = include_array_index,
                    always = always
                )
            )
        return self
    

    def unset(self, field:str=None, fields:list[str]|None=None)->"Pipeline":
        """
        Adds an unset stage to the current pipeline.
        
        Arguments:
        -------------------------------

            - field, str|None: field to be removed
            - fields, list[str]|None, list of fields to be removed
        
        """

        self.stages.append(
            Unset(field=field, fields=fields)
        )

        return self

if __name__ =="__main__":

    pipeline = Pipeline()
    pipeline.search(operator_name="text", query="test", path=["details", "id_epd", "id_serial", "name"] )
    
