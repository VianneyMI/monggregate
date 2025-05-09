import pytest
from pydantic import BaseModel as PydanticBaseModel
from monggregate.base import BaseModel, Expression, Singleton, express, isbasemodel


# Create a simple subclass of BaseModel for testing
class TestModel(BaseModel):
    field1: str = "default value"
    field2: int = 0

    @property
    def expression(self) -> Expression:
        return {"$add": [self.field1, self.field2]}


# Create a simple subclass of PydanticBaseModel for testing
class TestPydanticModel(PydanticBaseModel):
    field1: str = "default value"
    field2: int = 0


def test_singleton_instantiation():
    """Test that Singleton class can be instantiated correctly."""

    # Create two instances of the Singleton class
    instance1 = Singleton()
    instance2 = Singleton()

    # Check that both instances are the same object
    assert instance1 is instance2


def test_base_model_instantiation():
    """Test that BaseModel class can be instantiated correctly."""

    # Instantiate the model
    model = TestModel()

    # Check the default values
    assert model.field1 == "default value"
    assert model.field2 == 0

    # Test with custom values
    custom_model = TestModel(field1="custom", field2=42)
    assert custom_model.field1 == "custom"
    assert custom_model.field2 == 42


def test_isbasemodel():
    """Test that isbasemodel function works correctly."""

    # Instantiate the model
    test_model = TestModel()
    test_pydantic_model = TestPydanticModel()

    # Check that the model is a BaseModel
    assert isbasemodel(test_model)

    # Check that a non-BaseModel object is not a BaseModel
    assert not isbasemodel(42)

    # Check that a PydanticBaseModel is not a BaseModel
    assert not isbasemodel(test_pydantic_model)


class TestExpress:
    """Test that express function works correctly."""

    def test_with_basemodel_instance(self):
        """Test that express function works correctly for BaseModel objects."""

        # Instantiate the model
        test_model = TestModel()

        # Check that the expression is correct
        assert express(test_model) == {"$add": ["default value", 0]}

    def test_with_list_of_basemodel_instances(self):
        """Test that express function works correctly for a list of BaseModel objects."""

        # Instantiate the model
        test_model_1 = TestModel()
        test_model_2 = TestModel()

        # Create a list of the models
        test_model_list = [test_model_1, test_model_2]

        # Check that the expression is correct
        assert express(test_model_list) == [
            {"$add": ["default value", 0]},
            {"$add": ["default value", 0]},
        ]

    def test_with_dict_of_basemodel_instances(self):
        """Test that express function works correctly for a dictionary of BaseModel objects."""

        # Instantiate the model
        test_model = TestModel()
        unresolved_expression = {"$add": [test_model, 0]}

        # Check that the expression is correct
        # fmt: off
        assert express(unresolved_expression) == {
            "$add": [
                {"$add": ["default value", 0]}, 
                0],
        }
        # fmt: on

    @pytest.mark.xfail(
        reason="This comes from an issue in the recursion of the express function."
    )
    def test_with_nested_basemodel_instances(self):
        """Test that express function works correctly for a nested BaseModel object."""

        # Instantiate the model
        test_model = TestModel()
        unresolved_expression_layer_1 = {"$add": [test_model, 0]}
        unresolved_expression_layer_2 = {"$add": [unresolved_expression_layer_1, 0]}

        # Check that the expression is correct
        # fmt: off
        assert express(unresolved_expression_layer_2) == {
            "$add": [
                {
                    "$add": [
                        {"$add": ["default value", 0]},
                        0,
                    ]
                },
                0,
            ],
        }, express(unresolved_expression_layer_1)
        # fmt: on
