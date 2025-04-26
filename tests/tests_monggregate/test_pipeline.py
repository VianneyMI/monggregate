import pytest
from monggregate.pipeline import Pipeline


def test_pipeline_instantiation():
    """Test that Pipeline class can be instantiated correctly."""
    pipeline = Pipeline()

    # Check that the pipeline is initialized with an empty list of stages
    assert pipeline.stages == []

    # Check that the exported pipeline is also an empty list
    assert pipeline.export() == []

    # Check that the pipeline's expression property returns an empty list
    assert pipeline.expression == []
