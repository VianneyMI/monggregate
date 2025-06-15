import pytest
from monggregate.pipeline import Pipeline, Match, Project


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

    # Add tests for stages methods below
    #
    # ......


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
