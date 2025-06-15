import pytest
from monggregate.pipeline import Pipeline
from monggregate.stages import (
    AddFields,
    Bucket,
    BucketAuto,
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
    UnionWith,
    Unset,
    Unwind,
    VectorSearch,
)


class TestPipeline:
    """Test the Pipeline class."""

    def test_instantiation(self) -> None:
        """Test that Pipeline class can be instantiated correctly."""
        pipeline = Pipeline()

        # Check that the pipeline is initialized with an empty list of stages
        assert pipeline.stages == []

        # Check that the exported pipeline is also an empty list
        assert pipeline.export() == []

        # Check that the pipeline's expression property returns an empty list
        assert pipeline.expression == []

    def test___add__(self) -> None:
        """Test the __add__ method of the Pipeline class."""

        pipeline1 = Pipeline()
        pipeline2 = Pipeline()

        pipeline1.match(query={"name": "John"})
        pipeline2.project(fields=["name", "age"], include=True)

        combined_pipeline = pipeline1 + pipeline2

        # Check that the combined pipeline has two stages
        assert len(combined_pipeline.stages) == 2

        # Check that the first stage is a match stage
        assert isinstance(combined_pipeline.stages[0], Match)
        assert combined_pipeline.stages[0].expression == {"$match": {"name": "John"}}

        # Check that the second stage is a project stage
        assert isinstance(combined_pipeline.stages[1], Project)
        assert combined_pipeline.stages[1].expression == {
            "$project": {"name": 1, "age": 1}
        }

    def test___add_order_should_matter(self) -> None:
        """Test that the order of addition matters."""
        pipeline1 = Pipeline()
        pipeline2 = Pipeline()

        pipeline1.match(query={"name": "John"})
        pipeline2.project(fields=["name", "age"], include=True)

        combined_pipeline = pipeline1 + pipeline2
        reversed_combined_pipeline = pipeline2 + pipeline1

        assert combined_pipeline.export() != reversed_combined_pipeline.export()

    def test___add__with_non_pipeline_object(self) -> None:
        """Test the __add__ method of the Pipeline class with a non-Pipeline object."""
        pipeline = Pipeline()
        pipeline.match(query={"name": "John"})

        with pytest.raises(TypeError):
            pipeline + Project(fields=["name", "age"], include=True)

    def test___getitem__(self) -> None:
        """Test the __getitem__ method of the Pipeline class."""
        pipeline = Pipeline()
        pipeline.match(query={"name": "John"})
        pipeline.project(fields=["name", "age"], include=True)

        assert pipeline[0].expression == {"$match": {"name": "John"}}

    def test__getitem__index_out_of_range(self) -> None:
        """Test the __getitem__ method of the Pipeline class with edge cases."""

        pipeline = Pipeline()
        pipeline.match(query={"name": "John"})
        pipeline.project(fields=["name", "age"], include=True)

        # Edge case: get an item that doesn't exist
        with pytest.raises(IndexError):
            pipeline[2]

    def test__setitem__(self) -> None:
        """Test the __setitem__ method of the Pipeline class."""

        index = 0
        pipeline = Pipeline()

        pipeline.unwind(path="name")
        pipeline.match(query={"name": "John"})

        pipeline[index] = Project(fields=["name", "age"], include=True)

        assert isinstance(pipeline[index], Project)

    def test__setitem__index_out_of_range(self) -> None:
        """Test the __setitem__ method of the Pipeline class with edge cases."""

        index = 2
        pipeline = Pipeline()
        pipeline.unwind(path="name")
        pipeline.match(query={"name": "John"})

        with pytest.raises(IndexError):
            pipeline[index] = Project(fields=["name", "age"], include=True)

    def test__delitem__(self) -> None:
        """Test the __delitem__ method of the Pipeline class."""
        pipeline = Pipeline()
        pipeline.unwind(path="name")
        pipeline.match(query={"name": "John"})

        del pipeline[0]
        assert pipeline.export() == [{"$match": {"name": "John"}}]

    def test__len__(self) -> None:
        """Test the __len__ method of the Pipeline class."""

        pipeline = Pipeline()
        pipeline.unwind(path="name")
        pipeline.match(query={"name": "John"})

        assert len(pipeline) == 2

    def test_append(self) -> None:
        """Test the append method of the Pipeline class."""

        pipeline = Pipeline()
        pipeline.unwind(path="name")
        pipeline.match(query={"name": "John"})

        pipeline.append(Project(fields=["name", "age"], include=True))

        assert len(pipeline) == 3
        assert isinstance(pipeline[2], Project)

    def test_insert(self) -> None:
        """Test the insert method of the Pipeline class."""

        pipeline = Pipeline()
        pipeline.unwind(path="name")
        pipeline.match(query={"name": "John"})

        pipeline.insert(0, Project(fields=["name", "age"], include=True))

        assert len(pipeline) == 3

    def test_extend(self) -> None:
        """Test the extend method of the Pipeline class."""

        pipeline = Pipeline()
        pipeline.unwind(path="name")
        pipeline.match(query={"name": "John"})

        pipeline.extend([Project(fields=["name", "age"], include=True)])

    # ---------------------------------------------------
    # Stages
    # ---------------------------------------------------

    @pytest.mark.xfail(
        reason="""AddFields is implemented as a simple alias for Set stage,
                        which is correct, but it should be done in a different way here.
                        Indeed right now, the symbol is set to $set rather than $addFields.
                       
                       """
    )
    class TestAddFields:
        """Test the `add_fields` method of the Pipeline class."""

        def test_with_document(self) -> None:
            """Test the `add_fields` method of the Pipeline class with a document."""

            expected_first_stage = AddFields(document={"name": "John", "age": 30})

            pipeline = Pipeline()
            pipeline.add_fields(document={"name": "John", "age": 30})

            assert pipeline[0] == expected_first_stage
            assert pipeline.export() == [{"$addFields": {"name": "John", "age": 30}}]

        def test_with_kwargs(self) -> None:
            """Test the `add_fields` method of the Pipeline class with kwargs."""

            pipeline = Pipeline()
            pipeline.add_fields(name="John", age=30)

            assert pipeline.export() == [{"$addFields": {"name": "John", "age": 30}}]

    class TestBucket:
        """Test the `bucket` method of the Pipeline class."""

        def test_with_required_params(self) -> None:
            """Test the `bucket` method with required parameters."""

            pipeline = Pipeline()
            boundaries = [0, 10, 20, 50, 100]
            pipeline.bucket(by="price", boundaries=boundaries)

            expected_stage = Bucket(by="price", boundaries=boundaries)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Bucket)
            assert len(pipeline) == 1

        def test_with_group_by_param(self) -> None:
            """Test the `bucket` method with group_by parameter."""

            pipeline = Pipeline()
            boundaries = [0, 10, 20, 50, 100]
            pipeline.bucket(group_by="price", boundaries=boundaries)

            expected_stage = Bucket(by="price", boundaries=boundaries)
            assert pipeline[0] == expected_stage

        def test_with_default_param(self) -> None:
            """Test the `bucket` method with default parameter."""

            pipeline = Pipeline()
            boundaries = [0, 10, 20, 50, 100]
            default_value = "Other"
            pipeline.bucket(by="price", boundaries=boundaries, default=default_value)

            expected_stage = Bucket(
                by="price", boundaries=boundaries, default=default_value
            )
            assert pipeline[0] == expected_stage

        def test_with_output_param(self) -> None:
            """Test the `bucket` method with output parameter."""

            pipeline = Pipeline()
            boundaries = [0, 10, 20, 50, 100]
            output = {"count": {"$sum": 1}, "total": {"$sum": "$price"}}
            pipeline.bucket(by="price", boundaries=boundaries, output=output)

            expected_stage = Bucket(by="price", boundaries=boundaries, output=output)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that bucket method returns self for chaining."""

            pipeline = Pipeline()
            boundaries = [0, 10, 20, 50, 100]
            result = pipeline.bucket(by="price", boundaries=boundaries)

            assert result is pipeline
            assert len(pipeline) == 1

    class TestBucketAuto:
        """Test the `bucket_auto` method of the Pipeline class."""

        def test_with_required_params(self) -> None:
            """Test the `bucket_auto` method with required parameters."""

            pipeline = Pipeline()
            pipeline.bucket_auto(by="price", buckets=4)

            expected_stage = BucketAuto(by="price", buckets=4)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], BucketAuto)
            assert len(pipeline) == 1

        def test_with_group_by_param(self) -> None:
            """Test the `bucket_auto` method with group_by parameter."""

            pipeline = Pipeline()
            pipeline.bucket_auto(group_by="price", buckets=4)

            expected_stage = BucketAuto(by="price", buckets=4)
            assert pipeline[0] == expected_stage

        def test_with_output_param(self) -> None:
            """Test the `bucket_auto` method with output parameter."""

            pipeline = Pipeline()
            output = {"count": {"$sum": 1}, "total": {"$sum": "$price"}}
            pipeline.bucket_auto(by="price", buckets=4, output=output)

            expected_stage = BucketAuto(by="price", buckets=4, output=output)
            assert pipeline[0] == expected_stage

        def test_with_granularity_param(self) -> None:
            """Test the `bucket_auto` method with granularity parameter."""

            pipeline = Pipeline()
            from monggregate.stages import GranularityEnum

            pipeline.bucket_auto(by="price", buckets=4, granularity=GranularityEnum.R5)

            expected_stage = BucketAuto(
                by="price", buckets=4, granularity=GranularityEnum.R5
            )
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that bucket_auto method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.bucket_auto(by="price", buckets=4)

            assert result is pipeline
            assert len(pipeline) == 1

    class TestCount:
        """Test the `count` method of the Pipeline class."""

        def test_with_name(self) -> None:
            """Test the `count` method of the Pipeline class with a name."""

            expected_first_stage = Count(name="a_field")

            pipeline = Pipeline()
            pipeline.count(name="a_field")

            assert pipeline[0] == expected_first_stage
            assert pipeline.export() == [{"$count": "a_field"}]

    class TestExplode:
        """Test the `explode` method of the Pipeline class."""

        def test_with_path_to_array(self) -> None:
            """Test the `explode` method with path_to_array parameter."""

            pipeline = Pipeline()
            pipeline.explode(path_to_array="tags")

            expected_stage = Unwind(path_to_array="tags")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Unwind)

        def test_with_path(self) -> None:
            """Test the `explode` method with path parameter."""

            pipeline = Pipeline()
            pipeline.explode(path="tags")

            expected_stage = Unwind(path_to_array="tags")
            assert pipeline[0] == expected_stage

        def test_with_include_array_index(self) -> None:
            """Test the `explode` method with include_array_index parameter."""

            pipeline = Pipeline()
            pipeline.explode(path="tags", include_array_index="tag_index")

            expected_stage = Unwind(
                path_to_array="tags", include_array_index="tag_index"
            )
            assert pipeline[0] == expected_stage

        def test_with_always_parameter(self) -> None:
            """Test the `explode` method with always parameter."""

            pipeline = Pipeline()
            pipeline.explode(path="tags", always=True)

            expected_stage = Unwind(path_to_array="tags", always=True)
            assert pipeline[0] == expected_stage

        def test_with_preserve_null_and_empty_arrays(self) -> None:
            """Test the `explode` method with preserve_null_and_empty_arrays parameter."""

            pipeline = Pipeline()
            pipeline.explode(path="tags", preserve_null_and_empty_arrays=True)

            expected_stage = Unwind(path_to_array="tags", always=True)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that explode method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.explode(path="tags")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestGroup:
        """Test the `group` method of the Pipeline class."""

        def test_with_by_parameter(self) -> None:
            """Test the `group` method with by parameter."""

            pipeline = Pipeline()
            pipeline.group(by="category", query={"count": {"$sum": 1}})

            expected_stage = Group(by="category", query={"count": {"$sum": 1}})
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Group)

        def test_with_id_parameter(self) -> None:
            """Test the `group` method with _id parameter."""

            pipeline = Pipeline()
            pipeline.group(_id="category", query={"count": {"$sum": 1}})

            expected_stage = Group(by="category", query={"count": {"$sum": 1}})
            assert pipeline[0] == expected_stage

        def test_with_multiple_fields(self) -> None:
            """Test the `group` method with multiple grouping fields."""

            pipeline = Pipeline()
            pipeline.group(by=["category", "status"], query={"count": {"$sum": 1}})

            expected_stage = Group(
                by=["category", "status"], query={"count": {"$sum": 1}}
            )
            assert pipeline[0] == expected_stage

        def test_with_dict_grouping(self) -> None:
            """Test the `group` method with dictionary grouping."""

            pipeline = Pipeline()
            group_expr = {"category": "$category", "year": {"$year": "$date"}}
            pipeline.group(by=group_expr, query={"count": {"$sum": 1}})

            expected_stage = Group(by=group_expr, query={"count": {"$sum": 1}})
            assert pipeline[0] == expected_stage

        def test_with_no_grouping(self) -> None:
            """Test the `group` method with no grouping (aggregate all documents)."""

            pipeline = Pipeline()
            pipeline.group(by=None, query={"total": {"$sum": "$amount"}})

            expected_stage = Group(by=None, query={"total": {"$sum": "$amount"}})
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that group method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.group(by="category", query={"count": {"$sum": 1}})

            assert result is pipeline
            assert len(pipeline) == 1

    class TestLimit:
        """Test the `limit` method of the Pipeline class."""

        def test_with_value(self) -> None:
            """Test the `limit` method with a value."""

            pipeline = Pipeline()
            pipeline.limit(value=10)

            expected_stage = Limit(value=10)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Limit)
            assert pipeline.export() == [{"$limit": 10}]

        def test_with_large_value(self) -> None:
            """Test the `limit` method with a large value."""

            pipeline = Pipeline()
            pipeline.limit(value=1000000)

            expected_stage = Limit(value=1000000)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that limit method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.limit(value=5)

            assert result is pipeline
            assert len(pipeline) == 1

    class TestLookup:
        """Test the `lookup` method of the Pipeline class."""

        def test_with_basic_params(self) -> None:
            """Test the `lookup` method with basic parameters."""

            pipeline = Pipeline()
            pipeline.lookup(
                name="orders", right="orders", left_on="customer_id", right_on="_id"
            )

            expected_stage = Lookup(
                name="orders", right="orders", left_on="customer_id", right_on="_id"
            )
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Lookup)

        def test_with_on_parameter(self) -> None:
            """Test the `lookup` method with on parameter for equal field names."""

            pipeline = Pipeline()
            pipeline.lookup(name="user_data", right="users", on="user_id")

            expected_stage = Lookup(name="user_data", right="users", on="user_id")
            assert pipeline[0] == expected_stage

        def test_with_official_mongodb_names(self) -> None:
            """Test the `lookup` method with official MongoDB parameter names."""

            pipeline = Pipeline()
            pipeline.lookup(
                name="orders",
                right="orders",
                local_field="customer_id",
                foreign_field="_id",
            )

            expected_stage = Lookup(
                name="orders", right="orders", left_on="customer_id", right_on="_id"
            )
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that lookup method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.lookup(name="orders", right="orders", on="customer_id")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestMatch:
        """Test the `match` method of the Pipeline class."""

        def test_with_query_dict(self) -> None:
            """Test the `match` method with query dictionary."""

            pipeline = Pipeline()
            query = {"status": "active", "age": {"$gte": 18}}
            pipeline.match(query=query)

            expected_stage = Match(query=query)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Match)
            assert pipeline.export() == [{"$match": query}]

        def test_with_kwargs(self) -> None:
            """Test the `match` method with keyword arguments."""

            pipeline = Pipeline()
            pipeline.match(status="active", age=25)

            expected_query = {"status": "active", "age": 25}
            expected_stage = Match(query=expected_query)
            assert pipeline[0] == expected_stage

        def test_with_query_and_kwargs_combined(self) -> None:
            """Test the `match` method with both query dict and kwargs."""

            pipeline = Pipeline()
            pipeline.match(query={"status": "active"}, age=25, category="premium")

            expected_query = {"status": "active", "age": 25, "category": "premium"}
            expected_stage = Match(query=expected_query)
            assert pipeline[0] == expected_stage

        def test_with_empty_query(self) -> None:
            """Test the `match` method with empty query."""

            pipeline = Pipeline()
            pipeline.match()

            expected_stage = Match(query={})
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that match method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.match(status="active")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestOut:
        """Test the `out` method of the Pipeline class."""

        def test_with_collection_name(self) -> None:
            """Test the `out` method with collection name."""

            pipeline = Pipeline()
            pipeline.out(collection="result_collection")

            expected_stage = Out(collection="result_collection")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Out)

        def test_with_coll_parameter(self) -> None:
            """Test the `out` method with coll parameter."""

            pipeline = Pipeline()
            pipeline.out(coll="result_collection")

            expected_stage = Out(collection="result_collection")
            assert pipeline[0] == expected_stage

        def test_with_database_name(self) -> None:
            """Test the `out` method with database name."""

            pipeline = Pipeline()
            pipeline.out(collection="result_collection", db="analytics_db")

            expected_stage = Out(collection="result_collection", db="analytics_db")
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that out method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.out(collection="results")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestProject:
        """Test the `project` method of the Pipeline class."""

        def test_with_include_fields(self) -> None:
            """Test the `project` method with include fields."""

            pipeline = Pipeline()
            pipeline.project(fields=["name", "age"], include=True)

            expected_stage = Project(fields=["name", "age"], include=True)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Project)

        def test_with_exclude_fields(self) -> None:
            """Test the `project` method with exclude fields."""

            pipeline = Pipeline()
            pipeline.project(fields=["password", "internal_id"], exclude=True)

            expected_stage = Project(fields=["password", "internal_id"], exclude=True)
            assert pipeline[0] == expected_stage

        def test_with_projection_dict(self) -> None:
            """Test the `project` method with projection dictionary."""

            pipeline = Pipeline()
            projection = {
                "name": 1,
                "age": 1,
                "full_name": {"$concat": ["$first_name", " ", "$last_name"]},
            }
            pipeline.project(projection=projection)

            expected_stage = Project(projection=projection)
            assert pipeline[0] == expected_stage

        def test_with_kwargs(self) -> None:
            """Test the `project` method with keyword arguments."""

            pipeline = Pipeline()
            pipeline.project(name=1, age=1, status=0)

            expected_projection = {"name": 1, "age": 1, "status": 0}
            expected_stage = Project(projection=expected_projection)
            assert pipeline[0] == expected_stage

        def test_with_include_parameter_as_dict(self) -> None:
            """Test the `project` method with include as dictionary."""

            pipeline = Pipeline()
            include_dict = {"name": 1, "age": 1}
            pipeline.project(include=include_dict)

            expected_stage = Project(include=include_dict)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that project method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.project(fields=["name", "age"], include=True)

            assert result is pipeline
            assert len(pipeline) == 1

    class TestReplaceRoot:
        """Test the `replace_root` method of the Pipeline class."""

        def test_with_path(self) -> None:
            """Test the `replace_root` method with path parameter."""

            pipeline = Pipeline()
            pipeline.replace_root(path="user_info")

            expected_stage = ReplaceRoot(path="user_info")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], ReplaceRoot)

        def test_with_path_to_new_root(self) -> None:
            """Test the `replace_root` method with path_to_new_root parameter."""

            pipeline = Pipeline()
            pipeline.replace_root(path_to_new_root="user_info")

            expected_stage = ReplaceRoot(path="user_info")
            assert pipeline[0] == expected_stage

        def test_with_document(self) -> None:
            """Test the `replace_root` method with document parameter."""

            pipeline = Pipeline()
            doc = {"name": "$user.name", "email": "$user.email", "full_info": "$$ROOT"}
            pipeline.replace_root(document=doc)

            expected_stage = ReplaceRoot(document=doc)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that replace_root method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.replace_root(path="user_info")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestReplaceWith:
        """Test the `replace_with` method of the Pipeline class."""

        def test_with_path(self) -> None:
            """Test the `replace_with` method with path parameter."""

            pipeline = Pipeline()
            pipeline.replace_with(path="user_info")

            expected_stage = ReplaceRoot(path="user_info")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], ReplaceRoot)

        def test_with_path_to_new_root(self) -> None:
            """Test the `replace_with` method with path_to_new_root parameter."""

            pipeline = Pipeline()
            pipeline.replace_with(path_to_new_root="user_info")

            expected_stage = ReplaceRoot(path="user_info")
            assert pipeline[0] == expected_stage

        def test_with_document(self) -> None:
            """Test the `replace_with` method with document parameter."""

            pipeline = Pipeline()
            doc = {"name": "$user.name", "email": "$user.email"}
            pipeline.replace_with(document=doc)

            expected_stage = ReplaceRoot(document=doc)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that replace_with method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.replace_with(path="user_info")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestSample:
        """Test the `sample` method of the Pipeline class."""

        def test_with_value(self) -> None:
            """Test the `sample` method with a value."""

            pipeline = Pipeline()
            pipeline.sample(value=5)

            expected_stage = Sample(value=5)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Sample)

        def test_with_large_value(self) -> None:
            """Test the `sample` method with a large value."""

            pipeline = Pipeline()
            pipeline.sample(value=1000)

            expected_stage = Sample(value=1000)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that sample method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.sample(value=10)

            assert result is pipeline
            assert len(pipeline) == 1

    class TestSet:
        """Test the `set` method of the Pipeline class."""

        def test_with_document(self) -> None:
            """Test the `set` method with document parameter."""

            pipeline = Pipeline()
            document = {
                "full_name": {"$concat": ["$first_name", " ", "$last_name"]},
                "is_adult": {"$gte": ["$age", 18]},
            }
            pipeline.set(document=document)

            expected_stage = Set(document=document)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Set)

        def test_with_kwargs(self) -> None:
            """Test the `set` method with keyword arguments."""

            pipeline = Pipeline()
            pipeline.set(status="active", last_updated="$NOW")

            expected_document = {"status": "active", "last_updated": "$NOW"}
            expected_stage = Set(document=expected_document)
            assert pipeline[0] == expected_stage

        def test_with_document_and_kwargs(self) -> None:
            """Test the `set` method with both document and kwargs."""

            pipeline = Pipeline()
            document = {"computed_field": {"$add": ["$a", "$b"]}}
            pipeline.set(document=document, status="active", flag=True)

            expected_document = {
                "computed_field": {"$add": ["$a", "$b"]},
                "status": "active",
                "flag": True,
            }
            expected_stage = Set(document=expected_document)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that set method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.set(status="active")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestSkip:
        """Test the `skip` method of the Pipeline class."""

        def test_with_value(self) -> None:
            """Test the `skip` method with a value."""

            pipeline = Pipeline()
            pipeline.skip(value=10)

            expected_stage = Skip(value=10)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Skip)
            assert pipeline.export() == [{"$skip": 10}]

        def test_with_large_value(self) -> None:
            """Test the `skip` method with a large value."""

            pipeline = Pipeline()
            pipeline.skip(value=1000000)

            expected_stage = Skip(value=1000000)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that skip method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.skip(value=5)

            assert result is pipeline
            assert len(pipeline) == 1

    class TestSort:
        """Test the `sort` method of the Pipeline class."""

        def test_with_query_dict(self) -> None:
            """Test the `sort` method with query dictionary."""

            pipeline = Pipeline()
            query = {"name": 1, "age": -1}
            pipeline.sort(query=query)

            expected_stage = Sort(query=query)
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Sort)

        def test_with_ascending_fields(self) -> None:
            """Test the `sort` method with ascending fields."""

            pipeline = Pipeline()
            pipeline.sort(ascending=["name", "email"])

            expected_stage = Sort(ascending=["name", "email"])
            assert pipeline[0] == expected_stage

        def test_with_descending_fields(self) -> None:
            """Test the `sort` method with descending fields."""

            pipeline = Pipeline()
            pipeline.sort(descending=["created_date", "score"])

            expected_stage = Sort(descending=["created_date", "score"])
            assert pipeline[0] == expected_stage

        def test_with_by_parameter(self) -> None:
            """Test the `sort` method with by parameter."""

            pipeline = Pipeline()
            pipeline.sort(by=["name", "age"])

            expected_stage = Sort(by=["name", "age"])
            assert pipeline[0] == expected_stage

        def test_with_kwargs(self) -> None:
            """Test the `sort` method with keyword arguments."""

            pipeline = Pipeline()
            pipeline.sort(name=1, age=-1, score=1)

            expected_query = {"name": 1, "age": -1, "score": 1}
            expected_stage = Sort(query=expected_query)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that sort method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.sort(ascending=["name"])

            assert result is pipeline
            assert len(pipeline) == 1

    class TestSortByCount:
        """Test the `sort_by_count` method of the Pipeline class."""

        def test_with_field(self) -> None:
            """Test the `sort_by_count` method with a field."""

            pipeline = Pipeline()
            pipeline.sort_by_count(by="category")

            expected_stage = SortByCount(by="category")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], SortByCount)

        def test_with_expression(self) -> None:
            """Test the `sort_by_count` method with an expression."""

            pipeline = Pipeline()
            pipeline.sort_by_count(by="$status")

            expected_stage = SortByCount(by="$status")
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that sort_by_count method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.sort_by_count(by="category")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestUnionWith:
        """Test the `union_with` method of the Pipeline class."""

        def test_with_collection_name(self) -> None:
            """Test the `union_with` method with collection name."""

            pipeline = Pipeline()
            pipeline.union_with(collection="other_collection", coll=None)

            expected_stage = UnionWith(collection="other_collection")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], UnionWith)

        def test_with_coll_parameter(self) -> None:
            """Test the `union_with` method with coll parameter."""

            pipeline = Pipeline()
            pipeline.union_with(collection=None, coll="other_collection")

            expected_stage = UnionWith(collection="other_collection")
            assert pipeline[0] == expected_stage

        def test_with_pipeline(self) -> None:
            """Test the `union_with` method with pipeline parameter."""

            pipeline = Pipeline()
            union_pipeline = [
                {"$match": {"status": "active"}},
                {"$project": {"name": 1}},
            ]
            pipeline.union_with(
                collection="other_collection", coll=None, pipeline=union_pipeline
            )

            expected_stage = UnionWith(
                collection="other_collection", pipeline=union_pipeline
            )
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that union_with method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.union_with(collection="other_collection", coll=None)

            assert result is pipeline
            assert len(pipeline) == 1

    class TestUnwind:
        """Test the `unwind` method of the Pipeline class."""

        def test_with_path(self) -> None:
            """Test the `unwind` method with path parameter."""

            pipeline = Pipeline()
            pipeline.unwind(path="tags")

            expected_stage = Unwind(path="tags")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Unwind)

        def test_with_path_to_array(self) -> None:
            """Test the `unwind` method with path_to_array parameter."""

            pipeline = Pipeline()
            pipeline.unwind(path_to_array="tags")

            expected_stage = Unwind(path="tags")
            assert pipeline[0] == expected_stage

        def test_with_include_array_index(self) -> None:
            """Test the `unwind` method with include_array_index parameter."""

            pipeline = Pipeline()
            pipeline.unwind(path="tags", include_array_index="tag_index")

            expected_stage = Unwind(path="tags", include_array_index="tag_index")
            assert pipeline[0] == expected_stage

        def test_with_always_parameter(self) -> None:
            """Test the `unwind` method with always parameter."""

            pipeline = Pipeline()
            pipeline.unwind(path="tags", always=True)

            expected_stage = Unwind(path="tags", always=True)
            assert pipeline[0] == expected_stage

        def test_with_preserve_null_and_empty_arrays(self) -> None:
            """Test the `unwind` method with preserve_null_and_empty_arrays parameter."""

            pipeline = Pipeline()
            pipeline.unwind(path="tags", preserve_null_and_empty_arrays=True)

            expected_stage = Unwind(path="tags", always=True)
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that unwind method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.unwind(path="tags")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestUnset:
        """Test the `unset` method of the Pipeline class."""

        def test_with_single_field(self) -> None:
            """Test the `unset` method with a single field."""

            pipeline = Pipeline()
            pipeline.unset(field="password")

            expected_stage = Unset(field="password")
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], Unset)

        def test_with_multiple_fields(self) -> None:
            """Test the `unset` method with multiple fields."""

            pipeline = Pipeline()
            pipeline.unset(fields=["password", "internal_id", "temp_data"])

            expected_stage = Unset(fields=["password", "internal_id", "temp_data"])
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that unset method returns self for chaining."""

            pipeline = Pipeline()
            result = pipeline.unset(field="password")

            assert result is pipeline
            assert len(pipeline) == 1

    class TestVectorSearch:
        """Test the `vector_search` method of the Pipeline class."""

        def test_with_required_params(self) -> None:
            """Test the `vector_search` method with required parameters."""

            pipeline = Pipeline()
            query_vector = [0.1, 0.2, 0.3, 0.4, 0.5]
            pipeline.vector_search(
                index="vector_index",
                path="embedding",
                query_vector=query_vector,
                num_candidates=100,
                limit=10,
            )

            expected_stage = VectorSearch(
                index="vector_index",
                path="embedding",
                query_vector=query_vector,
                num_candidates=100,
                limit=10,
            )
            assert pipeline[0] == expected_stage
            assert isinstance(pipeline[0], VectorSearch)

        def test_with_filter(self) -> None:
            """Test the `vector_search` method with filter parameter."""

            pipeline = Pipeline()
            query_vector = [0.1, 0.2, 0.3, 0.4, 0.5]
            filter_dict = {"status": "active", "category": "premium"}
            pipeline.vector_search(
                index="vector_index",
                path="embedding",
                query_vector=query_vector,
                num_candidates=100,
                limit=10,
                filter=filter_dict,
            )

            expected_stage = VectorSearch(
                index="vector_index",
                path="embedding",
                query_vector=query_vector,
                num_candidates=100,
                limit=10,
                filter=filter_dict,
            )
            assert pipeline[0] == expected_stage

        def test_chaining(self) -> None:
            """Test that vector_search method returns self for chaining."""

            pipeline = Pipeline()
            query_vector = [0.1, 0.2, 0.3, 0.4, 0.5]
            result = pipeline.vector_search(
                index="vector_index",
                path="embedding",
                query_vector=query_vector,
                num_candidates=100,
                limit=10,
            )

            assert result is pipeline
            assert len(pipeline) == 1

    class TestMethodChaining:
        """Test method chaining across different stage methods."""

        def test_multiple_stages_chaining(self) -> None:
            """Test chaining multiple different stage methods."""

            pipeline = Pipeline()
            result = (
                pipeline.match(status="active")
                .project(fields=["name", "age"], include=True)
                .sort(ascending=["name"])
                .limit(value=10)
                .skip(value=5)
            )

            assert result is pipeline
            assert len(pipeline) == 5
            assert isinstance(pipeline[0], Match)
            assert isinstance(pipeline[1], Project)
            assert isinstance(pipeline[2], Sort)
            assert isinstance(pipeline[3], Limit)
            assert isinstance(pipeline[4], Skip)

        def test_complex_pipeline_chaining(self) -> None:
            """Test a complex pipeline with various stages."""

            pipeline = Pipeline()
            result = (
                pipeline.match(category="electronics")
                .lookup(name="user_info", right="users", on="user_id")
                .unwind(path="user_info")
                .group(
                    by="user_info.region", query={"total_sales": {"$sum": "$amount"}}
                )
                .sort(descending=["total_sales"])
                .limit(value=5)
            )

            assert result is pipeline
            assert len(pipeline) == 6


def test_pipeline_with_stages_and_raw_expressions() -> None:
    """Test that the Pipeline class can be instantiated with stages and raw expressions."""

    pipeline = Pipeline()
    pipeline.match(query={"name": "John"})

    assert pipeline.export() == [{"$match": {"name": "John"}}]

    pipeline.append(
        {
            "$redact": {
                "$cond": {
                    "if": {"$eq": ["$name", "John"]},
                    "then": "$$DESCEND",
                    "else": "$$PRUNE",
                }
            }
        },
    )

    assert pipeline.export() == [
        {"$match": {"name": "John"}},
        {
            "$redact": {
                "$cond": {
                    "if": {"$eq": ["$name", "John"]},
                    "then": "$$DESCEND",
                    "else": "$$PRUNE",
                }
            }
        },
    ]
