import pytest
from monggregate.base import BaseModel, Expression


def test_base_model_instantiation():
    """Test that BaseModel class can be instantiated correctly."""

    # Create a simple subclass of BaseModel for testing
    class TestModel(BaseModel):
        field1: str = "default value"
        field2: int = 0

    # Instantiate the model
    model = TestModel()

    # Check the default values
    assert model.field1 == "default value"
    assert model.field2 == 0

    # Test with custom values
    custom_model = TestModel(field1="custom", field2=42)
    assert custom_model.field1 == "custom"
    assert custom_model.field2 == 42
