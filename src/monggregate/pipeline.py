"""Pipeline Module"""

from typing import Any, Literal
from warnings import warn

from typing_extensions import Self

from monggregate import _run

from monggregate.base import BaseModel
from monggregate.stages import (
    AnyStage,
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
    SearchStageMap,
    Set,
    Skip,
    SortByCount,
    Sort,
    UnionWith,
    Unwind,
    Unset,
    VectorSearch,
)
from monggregate.stages.search.base import SearchBase, OperatorLiteral
from monggregate.search.operators import OperatorMap
from monggregate.search.operators.compound import Compound, ClauseType
from monggregate.search.collectors.facet import Facet, FacetType
from monggregate.search.commons import CountOptions, HighlightOptions
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

    # instance of pymongo or motor database to allow pipeline to directly runnable
    _db : _run.Database | _run.AsyncIOMotorDatabase | _run.MotorDatabase | None = None
    # name of the collection to run the pipeline on
    collection : str | None =None
    # list of stages that compose the pipeline
    stages : list[AnyStage] = []
   
    

    @property
    def statement(self)->list[dict]:
        """Returns the pipeline statement"""

        return [stage.statement for stage in self.stages]




    # ------------------------------------------------
    # Pipeline Internal Methods
    #-------------------------------------------------
    if _run.MOTOR:
        async def __call__(self)->list[dict[str, Any]]:
            """Makes a pipeline instance callable and executes the entire pipeline when called"""
    
            return await self.run()

        
        async def run(self)->list[dict[str, Any]]:
            """Executes the entire pipeline"""

            if self._db is None:
                raise ValueError("db is not defined. Please indicate which database to run the pipeline on")

            if not self.collection:
                raise ValueError("collection is not defined. Please indicate which collection to run the pipeline on")

            # TODO : Allow to yield results as they come in <VM, 08/09/2023>
            cursor = self._db[self.collection].aggregate(pipeline=self.export())
            array = await cursor.to_list(length=None)

            return array
        
    elif _run.PYMONGO:
        def __call__(self)->list[dict[str, Any]]:
            """Makes a pipeline instance callable and executes the entire pipeline when called"""
    
            return self.run()

        
        def run(self)->list[dict[str, Any]]:
            """Executes the entire pipeline"""

            if self._db is None:
                raise ValueError("_db is not defined. Please indicate which database to run the pipeline on")

            if not self.collection:
                raise ValueError("collection is not defined. Please indicate which collection to run the pipeline on")

            stages = self.export()
            array = list(self._db[self.collection].aggregate(pipeline=stages))
            return array
    else:
        def __call__(self)->None:
            self.run()
        
        def run(self)->None:
            raise NotImplementedError("No database driver found. Please install pymongo or motor")

    
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
    def __add__(self, other:Self)->Self:
        """Concatenates two pipelines together"""
        if not isinstance(other, Pipeline):
            raise TypeError(f"unsupported operand type(s) for +: 'Pipeline' and '{type(other)}'")
        
        return Pipeline(
            _db=self._db,
            collection=self.collection, 
            stages=self.stages + other.stages
            )
    
    def __getitem__(self, index:int)->AnyStage:
        """Returns a stage from the pipeline"""
        # https://realpython.com/inherit-python-list/
        return self.stages[index]

    def __setitem__(self, index:int, stage:AnyStage)->None:
        """Sets a stage in the pipeline"""
        self.stages[index] = stage

    def __delitem__(self, index:int)->None:
        """Deletes a stage from the pipeline"""
        del self.stages[index]

    def __len__(self)->int:
        """Returns the length of the pipeline"""
        return len(self.stages)
    
    def append(self, stage:AnyStage)->None:
        """Appends a stage to the pipeline"""
        self.stages.append(stage)

    def insert(self, index:int, stage:AnyStage)->None:
        """Inserts a stage in the pipeline"""
        self.stages.insert(index, stage)

    def extend(self, stages:list[AnyStage])->None:
        """Extends the pipeline with a list of stages"""
        self.stages.extend(stages)


    #---------------------------------------------------
    # Stages
    #---------------------------------------------------
    # The below methods wrap the constructors of the classes of the same name

    def add_fields(self, document:dict={}, **kwargs:Any)->Self:
        """
        Adds an add_fields stage to the current pipeline.

        Arguments:
        ---------------------------------
            - statement, dict :
            - document, dict : new fields to be added

        Online MongoDB documentation:
        -----------------------------
        Adds new fields to documents. set outputs documents that contain all existing fields from the inputs documents and newly added fields. Both stages are equivalent to a project stage that explicitly specifies all existing fields in the inputs documents and adds the new fields.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/set/#mongodb-pipeline-pipe.-set
        """

        document = document | kwargs
        self.stages.append(
            Set(document=document)
        )
        return self

    def bucket(self, *, boundaries:list, by:Any=None, group_by:Any=None, default:Any=None, output:dict|None=None)->Self:
        """
        Adds a bucket stage to the current pipeline.
        This stage aggregates documents into buckets specified by the boundaries argument.

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

        Online MongoDB documentation:
        ------------------------------
        Categorizes incoming documents into groups, called buckets, based on a specified expression and bucket boundaries and outputs a document per each bucket. Each output document contains an _id field whose value specifies the inclusive lower bound of the bucket. The
        output option specifies the fields included in each output document.

        $bucket only produces output documents for buckets that contain at least one input document.                           
        
        Source :  https://www.mongodb.com/docs/manual/meta/aggregation-quick-reference/
        """
        
        self.stages.append(
            Bucket(
                by = by or group_by,
                #group_by = group_by or by,
                boundaries = boundaries,
                default = default,
                output = output
            )
        )
        return self

    def bucket_auto(self, *, by:Any=None, group_by:Any=None, buckets:int, output:dict=None, granularity:GranularityEnum|None=None)->Self:
        """
        Adds a bucket_auto stage to the current pipeline.
        This stage aggregates documents into buckets automatically computed to statisfy the number of buckets desired
        and provided as an input.

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

        Online MongoDB documentation:
        -----------------------------
        Categorizes incoming documents into a specific number of groups, called buckets, based on a specified expression.
        Bucket boundaries are automatically determined in an attempt to evenly distribute the documents into the specified number of buckets.

        Each bucket is represented as a document in the output. The document for each bucket contains:

            * An _id object that specifies the bounds of the bucket.

                * The _id.min field specifies the inclusive lower bound for the bucket.

                * The _id.max field specifies the upper bound for the bucket. This bound is exclusive for all buckets except the final bucket in the series, where it is inclusive.

            * A count field that contains the number of documents in the bucket. The count field is included by default when the output document is not specified.
        
        Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/bucketAuto/
        """

        self.stages.append(
            BucketAuto(
                by = by or group_by,
                #group_by = group_by,
                buckets = buckets,
                output = output,
                granularity = granularity
            )
        )
        return self


    def count(self, name:str)->Self:
        """
        Adds a count stage to the current pipeline.
        Passes a document to the next stage that contains a count of the number of documents input to the stage.

        Arguments
        -------------------------------

            - name, str : name of the output field which the count as its value.
                        Must be a non-empty string, must not start with $, and must not contain the . character.

        Online MongoDB documentation:
        -----------------------------
        Passes a document to the next stage that contains a count of the number of documents input to the stage.

        $count has the following prototype form:
        >>> {"$count":"string"}

        <string> is the name of the output field which has the count as its value.
        <string> must be a non-empty string, must not start with $ and must not contain the . character.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/count/#mongodb-pipeline-pipe.-count
        """

        self.stages.append(
                Count(name=name)
            )
        return self

    def explode(self, \
                path_to_array:str|None=None, 
                path:str|None=None, 
                *,  
                include_array_index:str|None=None, 
                always:bool=False, 
                preserve_null_and_empty_arrays:bool=False)->Self:
        """
        Adds a unwind stage to the current pipeline.

        Arguments:
        ---------------------------------

            - path_to_array (path), str : path to an array field
            - include_array_index, str : name of a new field to hold the array index of the element
                                        NOTE : The name cannot start with a dollar sign
            - always (preserve_null_and_empty_index), bool : whether to output documents for input documents where the path does not resolve to a valid array. Defaults to False

        Online MongoDB documentation:
        -----------------------------
        Deconstructs an array field from the input documents to output a document for each element.
        Each output document is the input document with the value of the array field replaced by the element.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/#mongodb-pipeline-pipe.-unwind
        """

        self.stages.append(
                Unwind(
                    path=path,
                    include_array_index=include_array_index,
                    always=always
                    )
            )
        return self

    def group(self, *,  by:Any|None=None, _id:Any|None=None, query:dict={})->Self:
        """
        Adds a group stage to the current pipeline.
        The group stage separates documents into groups according to a "group key". The output is one document for each unique group key.
        The output documents can also contain additional fields that are set using accumulator expressions.
        
        Arguments:
        ------------------------
            - by,  str | list[str] | set[str] | dict | None : field or group of fields to group by
            - query, dict | None : Computed aggregated values (per group)

        Online MongoDB documentation:
        -----------------------------
        The $group stage separates documents into groups according to a "group key". The output is one document for each unique group key.

        A group key is often a field, or group of fields. The group key can also be the result of an expression. Use the _id field in the $group pipeline stage to set the group key. See below for
        usage examples.

        In the $group stage output, the _id field is set to the group key for that document.

        The output documents can also contain additional fields that are set using
        accumulator expressions.

        NOTE : The group stage does not order its output documents.

        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group
        """

        self.stages.append(
                Group(
                    by=by,
                    query=query
                )
            )
        return self

    def limit(self, value:int)->Self:
        """
        Adds a limit stage to the current pipeline.
        Limits the number of documents passed to the next stage in the pipeline.

        Arguments:
        ---------------------------------
            - value, int : the actual limit to apply.
                           limits the number of documents returned by the stage to
                           the provided value.

        Online MongoDB documentation:
        -----------------------------
        Limits the number of documents passed to the next stage in the pipeline.
        
        $limit takes a positive integer that specifies the maximum number of documents to pass along.

        NOTE : Starting in MongoDB 5.0, the $limit pipeline aggregation has a 64-bit integer limit. Values
        passed to the pipeline which exceed this limit will return a invalid argument error.

        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group
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
        local_field:str|None=None,
        right_on:str=None,
        foreign_field:str=None)->Self:
        """
        Adds a lookup stage to the current pipeline.
        Performs a left outer join to a collection in the same database to filter in documents from the "joined" collection for processing. The
        lookup stage adds a new array field to each input document. The new array field contains the matching documents from the "joined" collection. The
        lookup stage passes these reshaped documents to the next stage.
        
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

        Online MongoDB documentation:
        -----------------------------
        Performs a left outer join to a collection in the same database to filter in documents from the "joined" collection for processing. The lookup stage adds a new array field to each input document. The new array field contains the matching documents from the "joined" collection. The
        lookup stage passes these reshaped documents to the next stage.

        Starting in MongoDB 5.1, $lookup works across sharded collections.

        To combine elements from two different collections, use the $unionWith pipeline stage.

        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/#mongodb-pipeline-pipe.-lookup
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
            )->Self:
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

    def match(self, query:dict={}, expression:Any=None, **kwargs:Any)->Self:
        """
        Adds a match stage to the current pipeline.
        Filters the documents to pass only the documents that match the specified condition(s) to the next pipeline stage.

        Arguments:
        -------------------

            - query, dict : a simple MQL query use to filter the documents.
            - expression, Expression : an aggregation expression used to filter the documents
    
        NOTE : Use query if you're using a MQL query and expression if you're using aggregation expressions.

        Online MongoDB documentation:
        -----------------------------
        Filters the documents to pass only the documents that match the specified condition(s) to the next pipeline stage.
        
        $match takes a document that specifies the query conditions. The query syntax is identical to the read operation query syntax; i.e.
        $match does not accept raw aggregation expressions. Instead, use a $expr query expression to include aggregation expression in
        $match

        Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match

        """

        query = query | kwargs
        self.stages.append(
                Match(query=query, expression=expression)
            )
        return self

    def out(self, collection:str|None=None, coll:str|None=None, *, db:str|None=None)->Self:
        """
        Adds an out stage to the current pipeline.
        Takes the documents returned by the aggregation pipeline and writes them to a specified collection. Starting in MongoDB 4.4, you can specify the output database.

        Arguments:
        ---------------------------
            - db, str|None : name of the db to output the collection. Defaults to the current collection.
        - collection, str : name of the output collection

        Online MongoDB documentation:
        -----------------------------
        Takes the documents returned by the aggregation pipeline and writes them to a specified collection.
        The out stage must be the last stage in the pipeline. The out operator lets the aggregation framework return result sets of any size.

        WARNING : out replaces the specified collection if it exists.
        See [Replace Existing Collection](https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/#std-label-replace-existing-collection) for details.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out
        """

        self.stages.append(
            Out(
                collection=collection or coll,
                db = db
            )
        )
        return self

    def project(self, *,\
        include : str|set[str]|list[str]|dict|bool|None = None,
        exclude : str|set[str]|list[str]|dict|bool|None = None,
        fields : str|set[str]|list[str]|None = None,
        projection : dict = {},
        **kwargs:Any)->Self:
        """
        Adds a project stage to the current pipeline.
        Passes along the documents with the requested fields to the next stage in the pipeline. The specified fields can be existing fields from the input documents or newly computed fields.

        Arguments:
        ---------------------------
            - projection, dict | None : projection to be applied
            - fields, ProjectionArgs | None : fields  to be kept or excluded (depending on include/exclude parameters when those are booleans)
            - include, ProjectionArgs| dict | bool | None : fields to be kept
            - exclude, ProjectionArgs | dict | bool | None : fields to be excluded

        Online MongoDB documentation:
        -----------------------------
        Passes along the documents with the requested fields to the next stage in the pipeline. The specified fields can be existing fields from the input documents or newly computed fields.

        The $project takes a document that can specify the inclusion of fields,
        the suppression of the _id field, the addition of new fields, and the resetting of the values of existing fields. Alternatively, you may specify the exclusion of fields.

        The $project specifications have the following forms:
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project
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

    def replace_root(self, path:str|None=None, path_to_new_root:str|None=None, *,document:dict|None=None)->Self:
        """
        Adds a replace_root stage to the current pipeline.
        Replaces the input document with the specified document.
        The operation replaces all existing fields in the input document, including the _id field.
        You can promote an existing embedded document to the top level, or create a new document for promotion
        
        Arguments:
        -------------------------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - path_to_new_root, str|None : the path to the embedded document to be promoted
            - document, dict|None : document being created and to be set as the new root or expression

        Online MongoDB documentation:
        -----------------------------
        Replaces the input document with the specified document.
        The operation replaces all existing fields in the input document, including the _id field.
        You can promote an existing embedded document to the top level, or create a new document for promotion
        (see example:https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#std-label-new-replacement-doc).

        The replacement document can be any valid expression that resolves to a document.
        The stage errors and fails if <replacementDocument> is not a document. For more information on expressions, see Expressions.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#mongodb-pipeline-pipe.-replaceRoot
        """

        self.stages.append(
                ReplaceRoot(path=path, document=document)
            )
        return self

    def replace_with(self, path:str|None=None, path_to_new_root:str|None=None, *,document:dict|None=None)->Self:
        """
        Adds a replace_with stage to the current pipeline.

        Arguments:
        -------------------------------------

            - statement, dict : the statement generated during instantiation after parsing the other arguments
            - path_to_new_root, str|None : the path to the embedded document to be promoted
            - document, dict|None : document being created and to be set as the new root or expression

        Online MongoDB documentation:
        -----------------------------
        Replaces the input document with the specified document.
        The operation replaces all existing fields in the input document, including the _id field.
        You can promote an existing embedded document to the top level, or create a new document for promotion
        (see example:https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#std-label-new-replacement-doc).

        The replacement document can be any valid expression that resolves to a document.
        The stage errors and fails if <replacementDocument> is not a document. For more information on expressions, see Expressions.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#mongodb-pipeline-pipe.-replaceRoot
        """

        self.stages.append(
                ReplaceRoot(path=path, document=document)
            )
        return self

    def sample(self, value:int)->Self:
        """
        Adds a sample stage to the current pipeline.
        Randomly selects the specified number of documents from the input documents.

        Arguments:
        -----------------------
            - statement, dict : the statement generated after instantiation
            - value, int : positive integer representing the number of documents to be randomly picked. Defaults to 10.

        Online MongoDB documentation:
        -----------------------------
        Randomly selects the specified number of documents from the input documents.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sample/#mongodb-pipeline-pipe.-sample
        """

        self.stages.append(
                Sample(value=value)
            )
    
        return self
    
    # TODO : Check that clause_type and facet_type parameters don't break anything <VM, 04/11/2023>
    def search(
            self,
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,
            *,
            operator_name:OperatorLiteral|None=None,
            collector_name:Literal["facet"]|None=None,
            # Including the below parameters to give them visibility
            #---------------------------------------------------
            clause_type:ClauseType|None=None,
            facet_type:FacetType|None=None,
            #---------------------------------------------------
            index:str="default",
            count:CountOptions|None=None,
            highlight:HighlightOptions|None=None,
            return_stored_source:bool=False,
            score_details:bool=False,
            **kwargs:Any
    )->Self:
        """
        Adds a search stage to the current pipeline.
        The search stage performs a full-text search on the specified field or fields which must be covered by an Atlas Search index.

        NOTE : if used, search has to be the first stage of the pipeline

        Arguments:
        -------------------------------
            - path, str|list[str]|None : field to search in
            - query, str|list[str]|None : text to search for
            - index, str : name of the index to use for the search. Defaults to defaut
            - count, CountOptions|None : document that specifies the count options for retrieving
                                 a count of the results
            - highlight, HighlightOptions|None : document that specifies the highlight options for 
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
        
        Online MongoDB documentation:
        -----------------------------
        The search stage performs a full-text search on the specified field or fields 
        which must be covered by an Atlas Search index.

        Source : https://www.mongodb.com/docs/atlas/atlas-search/query-syntax/#mongodb-pipeline-pipe.-search
        """

        if not collector_name and not operator_name:
            operator_name = "text"

        
        # If pipeline is empty, adds a search stage
        if len(self) == 0:
            # if facet_type is not None:
            #     kwargs.update({"type":facet_type})
            # elif clause_type is not None:
            #     kwargs.update({"type":clause_type})

            self._init_search(
                search_class="search",
                operator_name=operator_name,
                collector_name=collector_name,
                path=path,
                query=query,
                index=index,
                count=count,
                highlight=highlight,
                return_stored_source=return_stored_source,
                score_details=score_details,
                **kwargs
            )
        
        # If pipeline is not empty then the first stage must be Search stage.
        # If so, adds the operator to the existing stage using Compound.
        elif len(self) >= 1 and isinstance(self.stages[0], Search):
            kwargs.update({
                # "collector_name":collector_name,
                "operator_name":operator_name,
                "path":path,
                "query":query,
            })
            has_facet_arg = self.__has_facet_arg(**kwargs)
            if has_facet_arg:
                self._append_facet(facet_type, **kwargs)
            else:
                self._append_clause(clause_type, **kwargs)

        else:
            raise TypeError("search stage has to be the first stage of the pipeline")
        
        return self
    

    def search_meta(
            self,
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,
            *,
            operator_name:OperatorLiteral|None=None,
            collector_name:Literal["facet"]|None=None,
            # Including the below parameters to give them visibility
            #---------------------------------------------------
            clause_type:ClauseType|None=None,
            facet_type:FacetType|None=None,
            #---------------------------------------------------
            index:str="default",
            count:CountOptions|None=None,
            highlight:HighlightOptions|None=None,
            return_stored_source:bool=False,
            score_details:bool=False,
            **kwargs:Any
    )->Self:
        """
        Adds a searchMeta stage to the current pipeline.
        The searchMeta stage returns different types of metadata result documents.
        
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
        
        if not collector_name and not operator_name:
            operator_name = "text"

        
        # If pipeline is empty, adds a search stage
        if len(self) == 0:
            self._init_search(
                search_class="searchMeta",
                operator_name=operator_name,
                collector_name=collector_name,
                path=path,
                query=query,
                index=index,
                count=count,
                highlight=highlight,
                return_stored_source=return_stored_source,
                score_details=score_details,
                **kwargs
            )
        
        # If pipeline is not empty then the first stage must be Search stage.
        # If so, adds the operator to the existing stage using Compound.
        elif len(self) >= 1 and isinstance(self.stages[0], SearchMeta):
            kwargs.update({
                # "collector_name":collector_name,
                "operator_name":operator_name,
                "path":path,
                "query":query,
            })
            has_facet_arg = self.__has_facet_arg(facet_type=facet_type, **kwargs)
            if has_facet_arg:
                self._append_facet(facet_type, **kwargs)
            else:
                self._append_clause(clause_type, **kwargs)

        else:
            raise TypeError("search stage has to be the first stage of the pipeline")

        return self


    def _init_search(
            self, 
            search_class:Literal["search", "searchMeta"], 
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,
            *,
            operator_name:OperatorLiteral|None=None,
            collector_name:Literal["facet"]|None=None,
            index:str="default",
            count:CountOptions|None=None,
            highlight:HighlightOptions|None=None,
            return_stored_source:bool=False,
            score_details:bool=False,
            **kwargs:Any)->None:
        """Adds a search stage to the pipeline."""

        if not collector_name and operator_name:
            search_stage = SearchStageMap[search_class].from_operator(
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
        else:
            search_stage = SearchStageMap[search_class].init_facet(
                operator_name=operator_name,
                path=path,
                query=query,
                index=index,
                count=count,
                highlight=highlight,
                return_stored_source=return_stored_source,
                score_details=score_details,
                collector_name=collector_name,
                **kwargs
            )

        self.stages.append(
            search_stage
        )

        return None


    def _append_clause(
            self, 
            clause_type:ClauseType|None=None,
            *,
            operator_name:OperatorLiteral|None=None,
            path:str|list[str]|None=None,
            query:str|list[str]|None=None,  
            **kwargs:Any)->None:
        """Adds a clause to the search stage of the pipeline."""

        first_stage = self.stages[0]
        if clause_type is None:
            clause_type = "should"

        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop("minimum_should_match", default_minimum_should_match)

        kwargs.update({
            "path":path,
            "query":query
        })

        if isinstance(first_stage.collector, Facet):
            if isinstance(first_stage.collector.operator, Compound):
                # Add clause to existing compound
                first_stage.__get_operators_map__(operator_name=operator_name)(clause_type, **kwargs)
            elif first_stage.collector.operator is None:
                # Create a compound operator with the to-be operator as a clause
                new_operator = Compound(minimum_should_match=minimum_should_match)
                new_operator.__get_operators_map__(operator_name=operator_name)(clause_type, **kwargs)
                first_stage.operator = new_operator  
            else:
                # Retrieve current operator and create a compound operator
                # and add the current operator as a clause
                new_operator = Compound(should=[first_stage.collector.operator], minimum_should_match=minimum_should_match)
                new_operator.__get_operators_map__(operator_name=operator_name)(clause_type, **kwargs)
                first_stage.operator = new_operator
        elif isinstance(first_stage.operator, Compound):
            # Add clause to existing compound
            first_stage.__get_operators_map__(operator_name=operator_name)(clause_type, **kwargs)
        elif first_stage.operator is not None:
            # Create a compound operator with the to-be operator as a clause
            new_operator = Compound(minimum_should_match=minimum_should_match)
            new_operator.__get_operators_map__(operator_name=operator_name)(clause_type, **kwargs)
            first_stage.operator = new_operator

        else:
            # Create an operator
            first_stage.operator = OperatorMap[operator_name](**kwargs)

        return None


    def _append_facet(self, facet_type:FacetType|None=None,  **kwargs:Any)->None:
        """Adds a facet to the search stage of the pipeline."""

        if not facet_type:
            facet_type = "string"

        first_stage = self.stages[0]
        operator = None
        if first_stage.operator is not None:
            operator = first_stage.operator
            first_stage.operator = None

        if not isinstance(first_stage.collector, Facet):
            first_stage.collector = Facet(operator=operator)

        first_stage.collector.facet(type=facet_type, **kwargs)


        return None


    @classmethod
    def __has_facet_arg(cls, **kwargs:Any)->bool:
        """Checks if the kwargs contains a facet argument"""

        facet_args = ["facet_type", "num_buckets", "boundaries", "default"]
        has_facet_arg = False

        for arg in facet_args:
            if arg in kwargs and kwargs[arg] is not None:
                has_facet_arg = True
                break

        return has_facet_arg
        
      
    def set(self, document:dict={}, **kwargs:Any)->Self:
        """
        Adds a set stage to the current pipeline.
        Adds new fields to documents. $set outputs documents that conain all existing fields from the inputs documents
        and newly added fields.
        Both stages are equivalent to a $project stage that explicitly specifies all existing fields in the inputs documents and adds the new fields.

        Arguments:
        ---------------------------------
            - statement, dict :
            - document, dict : new fields to be added

        Online MongoDB documentation:
        -----------------------------
        Adds new fields to documents. set outputs documents that contain all existing fields from the inputs documents and newly added fields. Both stages are equivalent to a project stage that explicitly specifies all existing fields in the inputs documents and adds the new fields.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/set/#mongodb-pipeline-pipe.-set
        """

        document = document | kwargs
        self.stages.append(
                Set(document=document)
            )
        return self

    def skip(self, value:int)->Self:
        """
        Adds a skip stage to the current pipeline.
        Skips over the specified number of documents that pass into the stage and passes the remaining documents to the next stage in the pipeline.

        Arguments:
        -----------------------
            - statement, dict : the statement generated after instantiation
            - value, int : positive integer representing the number of documents to be skipped.

        Online MongoDB documentation:
        -----------------------------
        Skips over the specified number of documents that pass into the stage and passes the remaining documents to the next stage in the pipeline.
        
        $skip takes a positive integer that specifies the maximum number of documents to skip.

        NOTE : Starting in MongoDB 5.0, the $skip pipeline aggregation has a 64-bit integer limit.
        Values passed to the pipeline which exceed this limit will return an invalid argument error.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/skip/#mongodb-pipeline-pipe.-skip
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
        **kwargs:Any)->Self:
        """
        Adds a sort stage to the current pipeline.
        Sorts all input documents and returns them to the pipeline in sorted order.
        
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

        Online MongoDB documentation:
        -----------------------------
        Sorts all input documents and returns them to the pipeline in sorted order.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort
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

    def sort_by_count(self, by:str)->Self:
        """
        Adds a sort_by_count stage to the current pipeline.
        Groups incoming documents based on the value of a specified expression, then computes the count of documents in each distinct group.

        Each output document contains two fields: an _id field containing the distinct grouping value,
        and a count field containing the number of documents belonging to that grouping or category.

        The documents are sorted by count in descending order.

        Arguments:
        -------------------------
            - _statement, dict : the statement generated during the validation process
            - by, str : the key to group, sort and count on

        Online MongoDB documentation:
        -----------------------------
        Groups incoming documents based on the value of a specified expression, then computes the count of documents in each distinct group.

        Each output document contains two fields: an _id field containing the distinct grouping value,
        and a count field containing the number of documents belonging to that grouping or category.

        The documents are sorted by count in descending order.

        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/sortByCount/#mongodb-pipeline-pipe.-sortByCount
        """

        self.stages.append(
                SortByCount(by=by)
            )
        return self
    
    def union_with(self, collection:str, coll:str, pipeline:list[dict]|None=None)->Self:
        """
        Adds a union_with stage to the current pipeline.
        Performs a union of two collections. unionWith combines pipeline results from two collections into a single result set. The stage outputs the combined result set (including duplicates) to the next stage.

        The order in which the combined result set documents are output is unspecified.
        Arguments:
        ---------------------------------
        
            - collection / coll, str : The collection or view whose pipeline results you wish to include in the result set
            - pipeline, list[dict] | Pipeline | None : An aggregation pipeline to apply to the specified coll.

        Online MongoDB documentation:
        -----------------------------
        Performs a union of two collections.
        unionWith combines pipeline results from two collections into a single result set. The stage outputs the combined result set (including duplicates) to the next stage.

        The order in which the combined result set documents are output is unspecified.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/unionWith/#mongodb-pipeline-pipe.-unionWith
        """

        self.stages.append(
            UnionWith(collection=collection, pipeline=pipeline)
        )

        return self

    def unwind(self, \
               path:str|None=None, 
               path_to_array:str|None=None, 
               include_array_index:str|None=None, 
               always:bool=False, 
               preserve_null_and_empty_arrays:bool=False)->Self:
        """
        Adds a unwind stage to the current pipeline.

        Arguments:
        ---------------------------------

            - path_to_array (path), str : path to an array field
            - include_array_index, str : name of a new field to hold the array index of the element
                                    NOTE : The name cannot start with a dollar sign
            - always (preserve_null_and_empty_index), bool : whether to output documents for input documents where the path does not resolve to a valid array. Defaults to False

        Online MongoDB documentation:
        -----------------------------
        Deconstructs an array field from the input documents to output a document for each element.
        Each output document is the input document with the value of the array field replaced by the element.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/#mongodb-pipeline-pipe.-unwind
        """

        self.stages.append(
                Unwind(
                    path = path or path_to_array,
                    include_array_index = include_array_index,
                    always = always or preserve_null_and_empty_arrays,
                )
            )
        return self
    

    def unset(self, field:str=None, fields:list[str]|None=None)->Self:
        """
        Adds an unset stage to the current pipeline.
        Removes/excludes fields from documents.
        
        Arguments:
        -------------------------------

            - field, str|None: field to be removed
            - fields, list[str]|None, list of fields to be removed
        
        Online MongoDB documentation:
        -----------------------------
        Removes/excludes fields from documents.
        
        Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/unset/#definition
        """

        self.stages.append(
            Unset(field=field, fields=fields)
        )

        return self
    

    def vector_search(
            self,
            index:str,
            path:str,
            query_vector:list[float],
            num_candidates:int,
            limit:int,
            filter:dict|None=None, 
            )->Self:
        """
        Adds a vector_search stage to the current pipeline.

        Arguments:
        ---------------------------------

            - index, str : name of the Atlas Vector Search index to use
            - path, str : path to the vector field to search
            - query_vector, list[float] : array of numbers of the BSON double type that represent the query vector
            - num_candidates, int : number of nearest neighbors to use during the search
            - limit, int : number of documents to return in the results
            - filter, dict|None : any MQL match expression that compares an indexed field with a boolean, number (not decimals), or string to use as a prefilter
        
        """

        self.stages.append(
            VectorSearch(
                index=index,
                path=path,
                query_vector=query_vector,
                num_candidates=num_candidates,
                limit=limit,
                filter=filter
            )
        
        )
        return self
