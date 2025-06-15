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

        # TODO : Implement several tests with different parameters
        #
        #
        #
        #
        #
        #

    class TestBucketAuto:
        """Test the `bucket_auto` method of the Pipeline class."""

        # TODO : Implement several tests with different parameters
        #
        #
        #
        #
        #
        #

    class TestCount:
        """Test the `count` method of the Pipeline class."""

        def test_with_name(self) -> None:
            """Test the `count` method of the Pipeline class with a name."""

            expected_first_stage = Count(name="a_field")

            pipeline = Pipeline()
            pipeline.count(name="a_field")

            assert pipeline[0] == expected_first_stage
            assert pipeline.export() == [{"$count": "a_field"}]


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
