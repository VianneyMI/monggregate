"""Pipeline Module"""

from typing import Any, Literal
from warnings import warn

from typing_extensions import Self


from monggregate.base import BaseModel, Expression
from monggregate.stages import (
    AnyStage,
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
    Stage,
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
from monggregate.stages.search.base import OperatorLiteral
from monggregate.search.operators import OperatorMap
from monggregate.search.operators.compound import Compound, ClauseType
from monggregate.search.collectors.facet import Facet, FacetType
from monggregate.search.commons import CountOptions, HighlightOptions
from monggregate.operators import MergeObjects
from monggregate.dollar import ROOT


class Pipeline(BaseModel):  # pylint: disable=too-many-public-methods
    """
    MongoDB aggregation pipeline abstraction.

    Parameters
    ----------
    stages : list[Stage]
        the list of Stages that the pipeline is made of.
        Similarly to the pipeline itself. This package constructs
        abstraction for MongoDB aggregation framework pipeline stages.

    Examples
    --------
    The following examples use the [example using MongoDB AirBnB demo dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-airbnb/#std-label-sample-airbnb).


    You can instantiate a pipeline instance as follow:

        >>> pipeline = Pipeline(collection="listingsAndReviews") # collection is the only mandatory attribute 
    
    and then add stages to the pipeline by calling its wrapper stages method as shown below:

        >>> pipeline.match(
            query = { "room_type": "Entire home/apt"}
        ).sort_by_count(
            by =  "bed_type"
        )

    and then use this pipeline in your own code:

        >>> db["listingsAndReviews"].aggregate(pipeline=pipeline()) # pipeline() here is actually equivalent to  pipeline.export()


    """

    stages: list[AnyStage | Expression] = []

    @property
    def expression(self) -> list[Expression]:
        """Returns the pipeline statement."""

        # TODO : Add test on this case <VM, 21/04/2024>
        # https://github.com/VianneyMI/monggregate/issues/106
        stages_expressions = []

        for stage in self.stages:
            if isinstance(stage, Stage):
                stages_expressions.append(stage.expression)
            else:
                stages_expressions.append(stage)

        return stages_expressions

    # ------------------------------------------------
    # Pipeline Internal Methods
    # -------------------------------------------------
    def export(self) -> list[dict]:
        """
        Exports current pipeline to pymongo format.

            >>> pipeline = Pipeline().match(...).project(...).limit(...).export()
            >>> db.examples.aggregate(pipeline=pipeline)

        """

        return self.expression

    # --------------------------------------------------
    # Pipeline List Methods
    # ---------------------------------------------------
    def __add__(self, other: Self) -> Self:
        """Concatenates two pipelines together."""
        if not isinstance(other, Pipeline):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Pipeline' and '{type(other)}'"
            )

        return Pipeline(stages=self.stages + other.stages)

    def __getitem__(self, index: int) -> AnyStage:
        """Returns a stage from the pipeline"""
        # https://realpython.com/inherit-python-list/
        return self.stages[index]

    def __setitem__(self, index: int, stage: AnyStage) -> None:
        """Sets a stage in the pipeline"""
        self.stages[index] = stage

    def __delitem__(self, index: int) -> None:
        """Deletes a stage from the pipeline"""
        del self.stages[index]

    def __len__(self) -> int:
        """Returns the length of the pipeline"""
        return len(self.stages)

    def append(self, stage: AnyStage) -> None:
        """Appends a stage to the pipeline."""
        self.stages.append(stage)

    def insert(self, index: int, stage: AnyStage) -> None:
        """Inserts a stage in the pipeline."""
        self.stages.insert(index, stage)

    def extend(self, stages: list[AnyStage]) -> None:
        """Extends the pipeline with a list of stages."""
        self.stages.extend(stages)

    # ---------------------------------------------------
    # Stages
    # ---------------------------------------------------
    # The below methods wrap the constructors of the classes of the same name

    def add_fields(self, document: dict = {}, **kwargs: Any) -> Self:
        """
        Adds an `add_fields` stage to the current pipeline.

        Parameters
        ----------
        document : dict
            new fields to be added

        Online MongoDB documentation
        ----------------------------
        Adds new fields to documents. `$addFields` outputs documents that contain all existing fields from the inputs documents and newly added fields. The `$addFields` stage is equivalent to a `$project` stage that explicitly specifies all existing fields in the inputs documents and adds the new fields.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/addFields)
        """

        document = document | kwargs
        self.stages.append(Set(document=document))
        return self

    def bucket(
        self,
        *,
        boundaries: list,
        by: str | list[str] | set[str] = None,
        group_by: str | list[str] | set[str] = None,
        default: Any = None,
        output: dict | None = None,
    ) -> Self:
        """
        Adds a `bucket` stage to the current pipeline.

        Parameters
        ----------
        boundaries : list
            An array of values that specify the boundaries for each bucket.
            Each adjacent pair of values acts as the inclusive lower boundary
            and the exclusive upper boundary for the bucket.
            NOTE : You must specify at least two boundaries.
        by : str or list[str] or set[str], optional
            field or fields to group the documents unless a default is provided,
            each input document must resolve the groupBy field path or
            expression to a value that falls within one of the ranges
            specified by the boundaries.
        group_by : str or list[str] or set[str], optional
            Alias for the parameter `by`.
        default : Any, optional
            A literal that specifies the `_id` (group name) of an additional
            bucket that contains all documents whoe groupBy expression result
            does not fall into a bucket specified by the boundaries. If
            unspecified, each input document must resolve groupBy expression
            to a value within one of the bucket ranges. The default value
            must be less than the lowest boundary or greather than or
            equal to the highest boundary value. The default value can
            be of a different type than the entries in boundaries.
        output : dict, optional
            A document that specifies the fields to include in the output documents in addition to
            the `_id` field. To specify the field to include you must use accumulator expressions:

                >>> {"outputField1" : {"accumulator":"expression1}}
                    ....
                    {"outputField2" : {"accumulator":"expression2}}

            If you do not specify an output document, the operation returns a count field containing
            the number of documents in each bucket.
            If you specify and output document, only the fields specified in the document are returned; i.e.
            the count field is not returned unless it is explicitly included in the output document.

        Returns
        -------
        self
            The pipeline object with the bucket stage added.

        Online MongoDB documentation
        ----------------------------
        Categorizes incoming documents into groups, called buckets, based
        on a specified expression and bucket boundaries and outputs a document
        per each bucket. Each output document contains an `_id` field whose
        value specifies the inclusive lower bound of the bucket. The output
        option specifies the fields included in each output document. `$bucket`
        only produces output documents for buckets that contain at least one input document.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/bucket)
        """

        self.stages.append(
            Bucket(
                by=by or group_by, 
                boundaries=boundaries, 
                default=default, 
                output=output
            )
        )
        return self

    def bucket_auto(
        self,
        *,
        by: str | list[str] | set[str] = None,
        group_by: str | list[str] | set[str] = None,
        buckets: int,
        output: dict | None = None,
        granularity: GranularityEnum | None = None,
    ) -> Self:
        """
        Adds a `bucket_auto` stage to the current pipeline.

        Parameters
        ----------
        by : str or list[str] or set[str], optional
            An expression to group documents. To specify a field path prefix
            the field name with a dollar sign `$` and enclose it in quotes.
        group_by : str or list[str] or set[str], optional
            Alias for the parameter `by`.
        buckets : int
            Number of buckets desired.
        output : dict
            A document that specifieds the fields to include in the oupput
            documents in addition to the `_id` field. To specify the field to
            include, you must use accumulator expressions.
            The defaut count field is not included in the output document
            when output is specified. Explicitly specify the count expression
            as part of the output document to include it:

                >>>    {
                        "outputfield1": { "accumulator": "expression1" },
                        ...
                        count: { $sum: 1 }
                        }
        granularity : monggregate.stages.GranularityEnum, optional
            A string that specifies the preferred number series to use to
            ensure that the calculated boundary edges end on preferred round
            numbers of their powers of 10. Available only if the all groupBy
            values are numeric and none of them are NaN. See [here](https://en.wikipedia.org/wiki/Preferred_number) for a definition of the preferred number.


        Online MongoDB documentation
        ----------------------------
        Categorizes incoming documents into a specific number of groups, called buckets, based on a specified expression.
        Bucket boundaries are automatically determined in an attempt to evenly distribute the documents into the specified number of buckets.

        Each bucket is represented as a document in the output. The document for each bucket contains:

        * An `_id` object that specifies the bounds of the bucket.

            * The `_id.min` field specifies the inclusive lower bound for the bucket.

            * The `_id.max` field specifies the upper bound for the bucket. This bound is exclusive for all buckets except the final bucket in the series, where it is inclusive.

        * A `count` field that contains the number of documents in the bucket. The `count` field is included by default when the output document is not specified.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/bucketAuto/)
        """

        self.stages.append(
            BucketAuto(
                by=by or group_by,
                buckets=buckets,
                output=output,
                granularity=granularity,
            )
        )
        return self

    def count(self, name: str) -> Self:
        """
        Adds a `count` stage to the current pipeline.

        Parameters
        ----------
        name: str
            Name of the output field which the count as its value.
            Must be a non-empty string, must not start with `$`, and must not contain the `.` character.

        Online MongoDB documentation
        ----------------------------
        Passes a document to the next stage that contains a count of the number of documents input to the stage.

        `$count` has the following prototype form:

            >>> {"$count":"string"}

        `string` is the name of the output field which has the count as its value.
        `string` must be a non-empty string, must not start with `$` and must not contain the `.` character.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/count)
        """

        self.stages.append(Count(name=name))
        return self

    def explode(
        self,
        path: str | None = None,
        path_to_array: str | None = None,
        *,
        include_array_index: str | None = None,
        always: bool = False,
        preserve_null_and_empty_arrays: bool = False,
    ) -> Self:
        """
        Adds a `unwind` stage to the current pipeline.

        Parameters
        ----------
        path : str | None
            Path to an array field.
        path_to_array : str | None
            Alias for `path`.
        include_array_index : str | None
            Name of a new field to hold the array index of the element.
            NOTE : The name cannot start with a dollar sign
        always :  bool
            Whether to output documents for input documents where the path
            does not resolve to a valid array. Defaults to False.
        preserve_null_and_empty_index : bool
            Alias for `always`.

        Online MongoDB documentation
        ----------------------------
        Deconstructs an array field from the input documents to output a document for each element.
        Each output document is the input document with the value of the array field replaced by the element.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind)
        """

        self.stages.append(
            Unwind(
                path=path or path_to_array,
                include_array_index=include_array_index,
                always=always or preserve_null_and_empty_arrays,
            )
        )
        return self

    def group(
        self, 
        *, 
        by: Any | None = None, 
        _id: Any | None = None, 
        query: dict = {}
    ) -> Self:
        """
        Adds a `group` stage to the current pipeline.

        Parameters
        ----------
        by : str | list[str] | set[str] | dict | None
            Field or group of fields to group by.
        _id : str | list[str] | set[str] | dict | None
            Alias for `by`.
        query :  dict | None
            Computed aggregated values (per group).

        Online MongoDB documentation
        -----------------------------
        The `$group` stage separates documents into groups according to a "group key". The output is one document for each unique group key.

        A group key is often a field, or group of fields. The group key can also be the result of an expression. Use the `_id` field in the `$group` pipeline stage to set the group key. See below for
        usage examples.

        In the `$group` stage output, the `_id` field is set to the group key for that document.

        The output documents can also contain additional fields that are set using
        accumulator expressions.

        NOTE : The group stage does not order its output documents.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/)
        """

        self.stages.append(Group(by=by or _id, query=query))
        return self

    def limit(self, value: int) -> Self:
        """
        Adds a `limit` stage to the current pipeline.

        Parameters
        ----------
        value : int
            the actual limit to apply. Limits the number of documents returned by the stage to the provided value.

        Online MongoDB documentation:
        -----------------------------
        Limits the number of documents passed to the next stage in the pipeline.

        `$limit` takes a positive integer that specifies the maximum number of documents to pass along.

        NOTE : Starting in MongoDB 5.0, the `$limit` pipeline aggregation has a 64-bit integer limit. Values
        passed to the pipeline which exceed this limit will return a invalid argument error.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/limit/)
        """

        self.stages.append(Limit(value=value))
        return self

    def lookup(
        self,
        *,
        name: str,
        right: str | None = None,
        on: str | None = None,
        left_on: str | None = None,
        local_field: str | None = None,
        right_on: str | None = None,
        foreign_field: str | None = None,
        let: dict | None,
        pipeline: list[dict] | None,
    ) -> Self:
        """
        Adds a `lookup` stage to the current pipeline.
        Performs a left outer join to a collection in the same database to filter in documents from the "joined" collection for processing. The
        `lookup` stage adds a new array field to each input document. The new array field contains the matching documents from the "joined" collection. The `lookup` stage passes these reshaped documents to the next stage.

        Parameters
        ----------
        name : str
            Name of the field containing the matches from the foreign collection.
        right : str | None
            Foreign collection.
        on : str | None
            Field to join both collections on.
        left_on : str | None
            Field of the current collection to join on.
        local_field : str | None
            Alias for `left_on` (official MongoDB name).
        right_on : str | None
            Field of the foreign collection to join on
        foreign_field : str | None
            Alias for `right_on`(official MongoDB name).
        let :  dict | None
            Variables to be used in the inner pipeline
        pipeline : list[dict] | None
            Pipeline to run on the foreign collection.


        NOTE (`pipeline` and `let` attributes) : To reference variables in pipeline stages, use the `$$<variable>` syntax.

        The `let` variables can be accessed by the stages in the pipeline, including additional `$lookup` stages nested in the pipeline.

        * A `$match` stage requires the use of an `$expr` operator to access the variables.
        The `$expr` operator allows the use of aggregation expressions inside of the `$match` syntax.

        Starting in MongoDB 5.0, the `$eq`, `$lt`, `$lte`, `$gt`, and `$gte` comparison operators placed in an
        `$expr` operator can use an index on the from collection referenced in a `$lookup` stage. Limitations:

            * Multikey indexes are not used.

            * Indexes are not used for comparisons where the operand is an array or the operand type is undefined.

            * Indexes are not used for comparisons with more than one field path operand.

        * Other (non-`$match`) stages in the pipeline do not require an
        `$expr` operator to access the variables.

        Online MongoDB documentation:
        -----------------------------
        Performs a left outer join to a collection in the same database to
        filter in documents from the "joined" collection for processing. The
        `$lookup` stage adds a new array field to each input document. The new
        array field contains the matching documents from the "joined" collection. The `$lookup` stage passes these reshaped documents to the next stage.

        Starting in MongoDB 5.1, `$lookup` works across sharded collections.

        To combine elements from two different collections, use the `$unionWith` pipeline stage.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/#mongodb-pipeline-pipe.-lookup)
        """

        self.stages.append(
            Lookup(
                name=name,
                right=right,
                on=on,
                left_on=left_on or local_field,
                right_on=right_on or foreign_field,
                let=let,
                pipeline=pipeline,
            )
        )
        return self

    def join(
        self,
        *,
        other: str,
        how: Literal[
            "left", "right", "inner"
        ] = "left",  # TODO : Implement outer and cross joins <VM, 10/04/2023>
        on: str | None = None,
        left_on: str | None = None,
        right_on: str | None = None,
    ) -> Self:
        """
        Adds a combination of stages, that together reproduce SQL joins.
        This is a virtual and unofficial stage. It is not documented on MongoDB aggregation pipeline reference page. As such, there is no Join class implementation in this package.

        Parameters
        ----------
        other : str
            Collection to join.
        how : {'left', 'right', 'inner'}
            Type of join to be performed. 'left' preserve the left
            collection. 'right' preserve the right collection. 'inner'
            returns only documents from the left collection that match
            documents from the right collection.
        on : str | None
            Key to use to perform the join, if the key name is the same
            in both collections.
        left_on : str|None
            Key to use on the left collection to perform the join.
            Must be use with right_on.
        right_on : str|None
            Key to use on the right collection to perform the join.
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
        elif how == "inner":
            self.__inner_join(right=other, on=on, left_on=left_on, right_on=right_on)

        return self

    def __join_common(
        self, right: str, on: str | None, left_on: str | None, right_on: str | None
    ) -> str:
        """Common parts between various join types"""

        _prefix = right.lower()
        join_field = "__" + _prefix + "__"
        self.stages.append(
            Lookup(
                right=right, on=on, left_on=left_on, right_on=right_on, name=join_field
            )
        )
        self.stages.append(Unwind(path_to_array=join_field))
        self.stages.append(
            ReplaceRoot(
                document=MergeObjects(operand=[ROOT, "$" + join_field]).expression
            )
        )
        self.stages.append(Project(exclude=join_field))
        return join_field

    def __left_join(
        self, right: str, on: str | None, left_on: str | None, right_on: str | None
    ) -> None:
        """Implements SQL left join"""

        self.__join_common(right=right, on=on, left_on=left_on, right_on=right_on)

    def __inner_join(
        self, right: str, on: str | None, left_on: str | None, right_on: str | None
    ) -> None:
        """Implements SQL inner join"""

        join_field = self.__join_common(
            right=right, on=on, left_on=left_on, right_on=right_on
        )

        filter_no_match = Match(
            query={join_field: []}
        )  # used to filter out documents in the left collection, that has no match in the right collection

        self.stages.insert(-3, filter_no_match)

    def match(self, query: dict = {}, expr: Expression = None, **kwargs: Any) -> Self:
        """
        Adds a `match` stage to the current pipeline.

        Parameters
        ----------
        query : dict
            A simple MQL query use to filter the documents.
        expr : dict[str, Any]
            An aggregation expression used to filter the documents

        NOTE : Use `query` if you're using a MQL query and `expression` if you're using aggregation expressions.

        Online MongoDB documentation
        ----------------------------
        Filters the documents to pass only the documents that match the specified condition(s) to the next pipeline stage.

        `$match` takes a document that specifies the query conditions. The query syntax is identical to the read operation query syntax; i.e.
        `$match` does not accept raw aggregation expressions. Instead, use a `$expr` query expression to include aggregation expression in
        `$match`.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match)

        """

        query = query | kwargs
        self.stages.append(Match(query=query, expr=expr))
        return self

    def out(
        self,
        collection: str | None = None,
        coll: str | None = None,
        *,
        db: str | None = None,
    ) -> Self:
        """
        Adds an `out` stage to the current pipeline.

        Parameters
        ----------
        collection : str | None
            Name of the output collection.
        coll : str | None
            Alias for `collection`.
        db : str | None
            Name of the db to output the collection. Defaults to the current collection.

        Online MongoDB documentation:
        -----------------------------
        Takes the documents returned by the aggregation pipeline and writes them to a specified collection. The `out` stage must be the last stage in the pipeline. The `out` operator lets the aggregation framework return result sets of any size.

        WARNING : `out` replaces the specified collection if it exists.
        See [Replace Existing Collection](https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/#std-label-replace-existing-collection) for details.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out)
        """

        self.stages.append(Out(collection=collection or coll, db=db))
        return self

    def project(
        self,
        *,
        include: str | set[str] | list[str] | dict | bool | None = None,
        exclude: str | set[str] | list[str] | dict | bool | None = None,
        fields: str | set[str] | list[str] | None = None,
        projection: dict = {},
        **kwargs: Any,
    ) -> Self:
        """
        Adds a `project` stage to the current pipeline.

        Parameters
        ----------
        include : str | set[str] | list[str] | dict | bool | None
            Fields to be kept.
        exclude : str | set[str] | list[str] | dict | bool | None
            Fields to be excluded.
        fields : str | set[str] | list[str] | None
            Fields  to be kept or excluded (depending on include/exclude parameters when those are booleans).
        projection : dict | None
            Projection to be applied.

        Online MongoDB documentation:
        -----------------------------
        Passes along the documents with the requested fields to the next stage in the pipeline. The specified fields can be existing fields from the input documents or newly computed fields.

        The `$project` takes a document that can specify the inclusion of fields, the suppression of the `_id` field, the addition of new fields, and the resetting of the values of existing fields. Alternatively, you may specify the exclusion of fields.

        The `$project` specifications have the following forms:

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project)
        """

        projection = projection | kwargs
        self.stages.append(
            Project(
                include=include, exclude=exclude, fields=fields, projection=projection
            )
        )
        return self

    def replace_root(
        self,
        path: str | None = None,
        path_to_new_root: str | None = None,
        *,
        document: dict | None = None,
    ) -> Self:
        """
        Adds a `replace_root` stage to the current pipeline.

        Parameters
        ----------
        path : str | None
            The path to the embedded document to be promoted.
        path_to_new_root : str|None
            Alias for `path`.
        document : dict | None
            Document being created and to be set as the new root or expression.

        Online MongoDB documentation:
        -----------------------------
        Replaces the input document with the specified document.
        The operation replaces all existing fields in the input document, including the `_id` field.
        You can promote an existing embedded document to the top level, or create a new document for promotion
        (see [example](https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#std-label-new-replacement-doc)).

        The replacement document can be any valid expression that resolves to a document. The stage errors and fails if <replacementDocument> is not a document. For more information on expressions, see [Expressions](https://www.mongodb.com/docs/manual/reference/operator/aggregation/#std-label-aggregation-expressions).

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#mongodb-pipeline-pipe.-replaceRoot)
        """

        self.stages.append(
            ReplaceRoot(path=path or path_to_new_root, document=document)
        )
        return self

    def replace_with(
        self,
        path: str | None = None,
        path_to_new_root: str | None = None,
        *,
        document: dict | None = None,
    ) -> Self:
        """
        Adds a `replace_with` stage to the current pipeline.

        Parameters
        ----------
        path : str | None
            The path to the embedded document to be promoted.
        path_to_new_root : str | None
            Alias for `path`.
        document : dict | None
            Document being created and to be set as the new root or expression.

        Online MongoDB documentation:
        -----------------------------
        Replaces the input document with the specified document.
        The operation replaces all existing fields in the input document, including the `_id` field.
        You can promote an existing embedded document to the top level, or create a new document for promotion
        (see [example](https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#std-label-new-replacement-doc)).

        The replacement document can be any valid expression that resolves to a document. The stage errors and fails if `<replacementDocument>` is not a document. For more information on expressions, see [Expressions](https://www.mongodb.com/docs/manual/reference/operator/aggregation/#std-label-aggregation-expressions).

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/replaceRoot/#mongodb-pipeline-pipe.-replaceRoot)
        """

        self.stages.append(
            ReplaceRoot(path=path or path_to_new_root, document=document)
        )
        return self

    def sample(self, value: int) -> Self:
        """
        Adds a `sample` stage to the current pipeline.

        Parameters
        ----------
        value : int
            Positive integer representing the number of documents to be randomly picked. Defaults to 10.

        Online MongoDB documentation:
        -----------------------------
        Randomly selects the specified number of documents from the input documents.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/sample/#mongodb-pipeline-pipe.-sample)
        """

        self.stages.append(Sample(value=value))

        return self

    # TODO : Check that clause_type and facet_type parameters don't break anything <VM, 04/11/2023>
    def search(
        self,
        path: str | list[str] | None = None,
        query: str | list[str] | None = None,
        *,
        operator_name: OperatorLiteral | None = None,
        collector_name: Literal["facet"] | None = None,
        # Including the below parameters to give them visibility
        # ---------------------------------------------------
        clause_type: ClauseType | None = None,
        facet_type: FacetType | None = None,
        # ---------------------------------------------------
        index: str = "default",
        count: CountOptions | None = None,
        highlight: HighlightOptions | None = None,
        return_stored_source: bool = False,
        score_details: bool = False,
        **kwargs: Any,
    ) -> Self:
        """
        Adds a `search` stage to the current pipeline.

        NOTE : if used, `search` has to be the first stage of the pipeline

        Parameters
        ----------
        path : str | list[str] | None
            Field to search in.
        query : str | list[str] | None
            Text to search for.
        operator_name : {"autocomplete","compound","equals","exists", "facet","more_like_this","range","regex","text", "wildcard"} | None
            Name of the operator to search with. Use the compound operator to  run a compound search (i.e query with multiple operators).
        collector_name : "facet" | None
            Name of the collector to use with the query. Value must be
            `facet` in case of a faceted search, `None` otherwise.
        facet_type : {'string', 'number', 'date}
            The type of the faceted fields in case of a faceted search.
        clause_type : {"must", "mustNot", "should", "filter"}
            The type of clause in case of a query with multiple operators.
        index : str
            Name of the index to use for the search. Defaults to default.
        count : CountOptions | None
            Document that specifies the count options for retrieving
            a count of the results.
        highlight : HighlightOptions | None
            Document that specifies the highlight options for displaying
            search terms in their original context.
        return_stored_source : bool
            Indicates whether to use the copy of the documents in the Atlas
            Search index (with just a subset of the fields) or to return the
            original full document (slower). Defaults to False. True => Use the copy
            False => Do a lookup and return the original documents.
        score_details : bool
            Indicates whether to retrieve the detailed breakdown of the score for
            the documents in the results. Defaults to False. To view the details,
            you must use the `$meta` expression in the `$project` stage.
        kwargs :  Any
            Operators specific options. Includes (non-exhaustive):
            - fuzzy, FuzzyOptions (controls fuzzy matching options)
            - score, dict (controls scoring options)
            - value, numeric|bool|date (for filtering)
            - allow_analyzed_field, bool (controls index scanning)
            - synonyms
            - like, dict|list[dict] (allow looking for similar documents).

        Online MongoDB documentation:
        -----------------------------
        The `search` stage performs a full-text search on the specified field or fields which must be covered by an Atlas Search index.

        [Source](https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/)
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
                **kwargs,
            )

        # If pipeline is not empty then the first stage must be Search stage.
        # If so, adds the operator to the existing stage using Compound.
        elif len(self) >= 1 and isinstance(self.stages[0], Search):
            kwargs.update(
                {
                    # "collector_name":collector_name,
                    "operator_name": operator_name,
                    "path": path,
                    "query": query,
                }
            )
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
        path: str | list[str] | None = None,
        query: str | list[str] | None = None,
        *,
        operator_name: OperatorLiteral | None = None,
        collector_name: Literal["facet"] | None = None,
        # Including the below parameters to give them visibility
        # ---------------------------------------------------
        clause_type: ClauseType | None = None,
        facet_type: FacetType | None = None,
        # ---------------------------------------------------
        index: str = "default",
        count: CountOptions | None = None,
        highlight: HighlightOptions | None = None,
        return_stored_source: bool = False,
        score_details: bool = False,
        **kwargs: Any,
    ) -> Self:
        """
        Adds a `search_meta` stage to the current pipeline.
    
        NOTE : if used, `search_meta` has to be the first stage of the pipeline

        Parameters
        ----------
        path : str|list[str]|None
            Field to search in.
        query : str|list[str]|None
            Text to search for.
        operator_name : {"autocomplete","compound","equals","exists", "facet","more_like_this","range","regex","text", "wildcard"}
            Name of the operator to search with. Use the compound operator to run a
            compound search (i.e query with multiple operators).
        collector_name : "facet" | None
            Name of the collector to use with the query. Value must be
            `facet` in case of a faceted search, `None` otherwise.
        facet_type : {'string', 'number', 'date}
            The type of the faceted fields in case of a faceted search.
        clause_type : {"must", "mustNot", "should", "filter"}
            The type of clause in case of a query with multiple operators.
        index : str
            Name of the index to use for the search. Defaults to default.
        count : CountOptions|None
            Document that specifies the count options for retrieving
            a count of the results.
        highlight : HighlightOptions|None
            Document that specifies the highlight options for displaying
            search terms in their original context.
        return_stored_source : bool
            Indicates whether to use the copy of the documents in the Atlas
            Search index (with just a subset of the fields) or to return the
            original full document (slower). Defaults to False. True => Use the copy
            False => Do a lookup and return the original documents.
        score_details : bool
            Indicates whether to retrieve the detailed breakdown of the score for
            the documents in the results. Defaults to False. To view the details,
            you must use the `$meta` expression in the `$project` stage.
        kwargs :  Any
            Operators specific options. Includes (non-exhaustive):
            - fuzzy, FuzzyOptions (controls fuzzy matching options)
            - score, dict (controls scoring options)
            - value, numeric|bool|date (for filtering)
            - allow_analyzed_field, bool (controls index scanning)
            - synonyms
            - like, dict|list[dict] (allow looking for similar documents).

        Online MongoDB documentation
        ----------------------------
        The `$searchMeta` stage returns different types of metadata result documents.
        
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
                **kwargs,
            )

        # If pipeline is not empty then the first stage must be Search stage.
        # If so, adds the operator to the existing stage using Compound.
        elif len(self) >= 1 and isinstance(self.stages[0], SearchMeta):
            kwargs.update(
                {
                    # "collector_name":collector_name,
                    "operator_name": operator_name,
                    "path": path,
                    "query": query,
                }
            )
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
        search_class: Literal["search", "searchMeta"],
        path: str | list[str] | None = None,
        query: str | list[str] | None = None,
        *,
        operator_name: OperatorLiteral | None = None,
        collector_name: Literal["facet"] | None = None,
        index: str = "default",
        count: CountOptions | None = None,
        highlight: HighlightOptions | None = None,
        return_stored_source: bool = False,
        score_details: bool = False,
        **kwargs: Any,
    ) -> None:
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
                **kwargs,
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
                **kwargs,
            )

        self.stages.append(search_stage)

        return None

    def _append_clause(
        self,
        clause_type: ClauseType | None = None,
        *,
        operator_name: OperatorLiteral | None = None,
        path: str | list[str] | None = None,
        query: str | list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Adds a clause to the search stage of the pipeline."""

        first_stage = self.stages[0]
        if clause_type is None:
            clause_type = "should"

        if clause_type == "should":
            default_minimum_should_match = 1
        else:
            default_minimum_should_match = 0

        minimum_should_match = kwargs.pop(
            "minimum_should_match", default_minimum_should_match
        )

        kwargs.update({"path": path, "query": query})

        if isinstance(first_stage.collector, Facet):
            if isinstance(first_stage.collector.operator, Compound):
                # Add clause to existing compound
                first_stage.__get_operators_map__(operator_name=operator_name)(
                    clause_type, **kwargs
                )
            elif first_stage.collector.operator is None:
                # Create a compound operator with the to-be operator as a clause
                new_operator = Compound(minimum_should_match=minimum_should_match)
                new_operator.__get_operators_map__(operator_name=operator_name)(
                    clause_type, **kwargs
                )
                first_stage.operator = new_operator
            else:
                # Retrieve current operator and create a compound operator
                # and add the current operator as a clause
                new_operator = Compound(
                    should=[first_stage.collector.operator],
                    minimum_should_match=minimum_should_match,
                )
                new_operator.__get_operators_map__(operator_name=operator_name)(
                    clause_type, **kwargs
                )
                first_stage.operator = new_operator
        elif isinstance(first_stage.operator, Compound):
            # Add clause to existing compound
            first_stage.__get_operators_map__(operator_name=operator_name)(
                clause_type, **kwargs
            )
        elif first_stage.operator is not None:
            # Create a compound operator with the to-be operator as a clause
            new_operator = Compound(minimum_should_match=minimum_should_match)
            new_operator.__get_operators_map__(operator_name=operator_name)(
                clause_type, **kwargs
            )
            first_stage.operator = new_operator

        else:
            # Create an operator
            first_stage.operator = OperatorMap[operator_name](**kwargs)

        return None

    def _append_facet(self, facet_type: FacetType | None = None, **kwargs: Any) -> None:
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
    def __has_facet_arg(cls, **kwargs: Any) -> bool:
        """Checks if the kwargs contains a facet argument"""

        facet_args = ["facet_type", "num_buckets", "boundaries", "default"]
        has_facet_arg = False

        for arg in facet_args:
            if arg in kwargs and kwargs[arg] is not None:
                has_facet_arg = True
                break

        return has_facet_arg

    def set(self, document: dict = {}, **kwargs: Any) -> Self:
        """
        Adds a `set` stage to the current pipeline.

        Parameters
        ----------
        document : dict
            New fields to be added.

        Online MongoDB documentation:
        -----------------------------
        Adds new fields to documents. `$set` outputs documents that contain all existing fields from the inputs documents and newly added fields. Both stages are equivalent to a `$project` stage that explicitly specifies all existing fields in the inputs documents and adds the new fields.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/set/#mongodb-pipeline-pipe.-set)
        """

        document = document | kwargs
        self.stages.append(Set(document=document))
        return self

    def skip(self, value: int) -> Self:
        """
        Adds a `skip` stage to the current pipeline.

        Parameters
        ----------
        value : int
            Positive integer representing the number of documents to be skipped.

        Online MongoDB documentation:
        -----------------------------
        Skips over the specified number of documents that pass into the
        stage and passes the remaining documents to the next stage in the
        pipeline.

        `$skip` takes a positive integer that specifies the maximum number of documents to skip.

        NOTE : Starting in MongoDB 5.0, the `$skip` pipeline aggregation has a 64-bit integer limit.
        Values passed to the pipeline which exceed this limit will return an invalid argument error.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/skip/#mongodb-pipeline-pipe.-skip)
        """

        self.stages.append(Skip(value=value))
        return self

    def sort(
        self,
        *,
        descending: str | list[str] | dict | bool | None = None,
        ascending: str | list[str] | dict | bool | None = None,
        by: list[str] | None = None,
        query: dict[str, Literal[1, -1]] = {},
        **kwargs: Any,
    ) -> Self:
        """
        Adds a `sort` stage to the current pipeline.

        Parameters
        ----------
        descending : set[str] | dict | None
            Fields to sort on descending order on.
        ascending : set[str] | dict | None
            Fields to sort on ascending order on.
        by : list[str] | None
            Fields to sort on. If sorting on multiple fields, sort order is
            evaluated from left to right.
        query : dict
            Fields-sort order mapping. 1 for ascending order, -1 for descending
            order. Defaults to {} if not provided, the query will be built from
            ascending and descending parameters.

        NOTE : When trying to sort on several fields and opposite orders use
        `query` rather than using `ascending` and `descending` simunateously.

        WARNING : If using the `ascending` and `descending` parameters at the same time, the generated query will have the following form:

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
        Sorts all input documents and returns them to the pipeline in sorted
        order.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort)
        """

        query = query | kwargs
        self.stages.append(
            Sort(descending=descending, ascending=ascending, by=by, query=query)
        )
        return self

    def sort_by_count(self, by: str) -> Self:
        """
        Adds a `sort_by_count` stage to the current pipeline.

        Parameters
        ----------
        by : str
            The key to group, sort and count on.

        Online MongoDB documentation:
        -----------------------------
        Groups incoming documents based on the value of a specified
        expression, then computes the count of documents in each distinct
        group.

        Each output document contains two fields: an `_id` field containing the
        distinct grouping value, and a `count` field containing the number of
        documents belonging to that grouping or category.

        The documents are sorted by count in descending order.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/sortByCount/#mongodb-pipeline-pipe.-sortByCount)
        """

        self.stages.append(SortByCount(by=by))
        return self

    def union_with(
        self, collection: str, coll: str, pipeline: list[dict] | None = None
    ) -> Self:
        """
        Adds a `union_with` stage to the current pipeline.

        Parameters
        ----------
        collection : str
            The collection or view whose pipeline results you wish to include in
            the result set.
        coll : str
            Alias for `collection`.
        pipeline : list[dict] | None
            An aggregation pipeline to apply to the specified coll.

        Online MongoDB documentation:
        -----------------------------
        Performs a union of two collections. `unionWith` combines pipeline results from two collections into a single result set. The stage outputs the combined result set (including duplicates) to the next stage.

        The order in which the combined result set documents are output is
        unspecified.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/unionWith/#mongodb-pipeline-pipe.-unionWith)
        """

        self.stages.append(UnionWith(collection=collection or coll, pipeline=pipeline))

        return self

    def unwind(
        self,
        path: str | None = None,
        path_to_array: str | None = None,
        include_array_index: str | None = None,
        always: bool = False,
        preserve_null_and_empty_arrays: bool = False,
    ) -> Self:
        """
        Adds a `unwind` stage to the current pipeline.

        Parameters
        ----------
        path : str | None
            Path to an array field.
        path_to_array : str | None
            Alias for `path`.
        include_array_index :  str | None
            Name of a new field to hold the array index of the element.
            NOTE : The name cannot start with a dollar sign.
        always : bool
            Whether to output documents for input documents where the path does
            not resolve to a valid array. Defaults to False.
        preserve_null_and_empty_index : bool
            Alias for `always`.

        Online MongoDB documentation:
        -----------------------------
        Deconstructs an array field from the input documents to output a
        document for each element. Each output document is the input document
        with the value of the array field replaced by the element.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/#mongodb-pipeline-pipe.-unwind)
        """

        self.stages.append(
            Unwind(
                path=path or path_to_array,
                include_array_index=include_array_index,
                always=always or preserve_null_and_empty_arrays,
            )
        )
        return self

    def unset(self, field: str | None = None, fields: list[str] | None = None) -> Self:
        """
        Adds an `unset` stage to the current pipeline.

        Parameters
        ----------
        field : str | None
            Field to be removed.
        fields : list[str] | None
            List of fields to be removed.

        Online MongoDB documentation:
        -----------------------------
        Removes/excludes fields from documents.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/unset/#definition)
        """

        self.stages.append(Unset(field=field, fields=fields))

        return self

    def vector_search(
        self,
        index: str,
        path: str,
        query_vector: list[float],
        num_candidates: int,
        limit: int,
        filter: dict | None = None,
    ) -> Self:
        """
        Adds a `vector_search` stage to the current pipeline.

        Parameters
        ----------
        index : str
            Name of the Atlas Vector Search index to use.
        path : str
            Path to the vector field to search.
        query_vector : list[float]
            Array of numbers of the BSON double type that represent the query vector.
        num_candidates : int
            Number of nearest neighbors to use during the search.
        limit : int
            Number of documents to return in the results.
        filter : dict|None
            Any MQL match expression that compares an indexed field with a boolean, number (not decimals), or string to use as a prefilter.

        Online MongoDB documentation
        ----------------------------
        `$vectorSearch` performs a semantic search on data in your Atlas cluster. If you store vector embeddings that are less than or equal to 4096 dimensions in width for any kind of data along with other data in your collection on the Atlas cluster, you can seamlessly index the vector data along with your other data. You can then use the `$vectorSearch` stage to pre-filter your data and perform semantic search against the indexed fields. See:

        * [Index Vector Embeddings](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type/) to learn more about creating Atlas Vector Search indexes.

        * [Vector Search Queries](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/) to learn more about [$vectorSearch](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/#mongodb-pipeline-pipe.-vectorSearch) pipeline stage syntax and usage.

        [Source](https://www.mongodb.com/docs/manual/reference/operator/aggregation/vectorSearch/)
        """

        self.stages.append(
            VectorSearch(
                index=index,
                path=path,
                query_vector=query_vector,
                num_candidates=num_candidates,
                limit=limit,
                filter=filter,
            )
        )
        return self
