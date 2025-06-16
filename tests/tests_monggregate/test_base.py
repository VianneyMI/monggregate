from pydantic import BaseModel as PydanticBaseModel
from monggregate.base import BaseModel, Expression, Singleton, express, isbasemodel


# Create a simple subclass of BaseModel for testing
class DummyModel(BaseModel):
    field1: str = "default value"
    field2: int = 0

    @property
    def expression(self) -> Expression:
        return {"$dummy": [self.field1, self.field2]}


# Create a simple subclass of PydanticBaseModel for testing
class DummyPydanticModel(PydanticBaseModel):
    field1: str = "default value"
    field2: int = 0


def test_singleton_instantiation() -> None:
    """Test that Singleton class can be instantiated correctly."""

    # Create two instances of the Singleton class
    instance1 = Singleton()
    instance2 = Singleton()

    # Check that both instances are the same object
    assert instance1 is instance2


def test_base_model_instantiation() -> None:
    """Test that BaseModel class can be instantiated correctly."""

    # Instantiate the model
    model = DummyModel()

    # Check the default values
    assert model.field1 == "default value"
    assert model.field2 == 0

    # Test with custom values
    custom_model = DummyModel(field1="custom", field2=42)
    assert custom_model.field1 == "custom"
    assert custom_model.field2 == 42


def test_isbasemodel() -> None:
    """Test that isbasemodel function works correctly."""

    # Instantiate the model
    test_model = DummyModel()
    test_pydantic_model = DummyPydanticModel()

    # Check that the model is a BaseModel
    assert isbasemodel(test_model)

    # Check that a non-BaseModel object is not a BaseModel
    assert not isbasemodel(42)

    # Check that a PydanticBaseModel is not a BaseModel
    assert not isbasemodel(test_pydantic_model)


class TestExpress:
    """Test that express function works correctly."""

    def test_with_basemodel_instance(self) -> None:
        """Test that express function works correctly for BaseModel objects."""

        # Instantiate the model
        test_model = DummyModel()

        # Check that the expression is correct
        assert express(test_model) == {"$dummy": ["default value", 0]}

    def test_with_list_of_basemodel_instances(self) -> None:
        """Test that express function works correctly for a list of BaseModel objects."""

        # Instantiate the model
        test_model_1 = DummyModel()
        test_model_2 = DummyModel()

        # Create a list of the models
        test_model_list = [test_model_1, test_model_2]

        # Check that the expression is correct
        assert express(test_model_list) == [
            {"$dummy": ["default value", 0]},
            {"$dummy": ["default value", 0]},
        ]

    def test_with_dict_of_basemodel_instances(self) -> None:
        """Test that express function works correctly for a dictionary of BaseModel objects."""

        # Instantiate the model
        test_model = DummyModel()
        unresolved_expression = {"$add": [test_model, 0]}

        # Check that the expression is correct
        # fmt: off
        assert express(unresolved_expression) == {
            "$add": [
                {"$dummy": ["default value", 0]}, 
                0],
        }
        # fmt: on

    def test_with_nested_basemodel_instances(self) -> None:
        """Test that express function works correctly for a nested BaseModel object."""

        # Instantiate the model
        test_model = DummyModel()
        unresolved_expression_nested_layer = {"$add": [test_model, 0]}
        unresolved_expression_top_layer = {
            "$add": [unresolved_expression_nested_layer, 1]
        }

        # Check that the expression is correct
        # fmt: off
        assert express(unresolved_expression_top_layer) == {
            "$add": [
                {
                    "$add": [
                        {"$dummy": ["default value", 0]},
                        0,
                    ]
                },
                1,
            ],
        }, express(unresolved_expression_top_layer)
        # fmt: on

    def test_with_primitive_types(self) -> None:
        """Test that express function works correctly with primitive types."""

        # Test various primitive types
        assert express(42) == 42
        assert express("hello") == "hello"
        assert express(True) is True
        assert express(False) is False
        assert express(None) is None
        assert express(3.14) == 3.14

    def test_with_empty_containers(self) -> None:
        """Test that express function works correctly with empty containers."""

        # Test empty list and dict
        assert express([]) == []
        assert express({}) == {}

    def test_with_mixed_list_types(self) -> None:
        """Test that express function works correctly with lists containing mixed types."""

        test_model = DummyModel()
        mixed_list = [test_model, 42, "hello", None, {"key": "value"}]

        expected = [
            {"$dummy": ["default value", 0]},
            42,
            "hello",
            None,
            {"key": "value"},
        ]

        assert express(mixed_list) == expected

    def test_with_deeply_nested_structures(self) -> None:
        """Test that express function works correctly with deeply nested structures."""

        test_model = DummyModel()
        deeply_nested = {
            "level1": {"level2": {"level3": [test_model, {"level4": test_model}]}}
        }

        expected = {
            "level1": {
                "level2": {
                    "level3": [
                        {"$dummy": ["default value", 0]},
                        {"level4": {"$dummy": ["default value", 0]}},
                    ]
                }
            }
        }

        assert express(deeply_nested) == expected

    def test_with_list_of_dicts_containing_basemodels(self) -> None:
        """Test that express function works correctly with lists of dictionaries containing BaseModels."""

        test_model1 = DummyModel(field1="first", field2=1)
        test_model2 = DummyModel(field1="second", field2=2)

        list_of_dicts = [
            {"operation": "$add", "operands": [test_model1, 10]},
            {"operation": "$multiply", "operands": [test_model2, 5]},
        ]

        expected = [
            {"operation": "$add", "operands": [{"$dummy": ["first", 1]}, 10]},
            {"operation": "$multiply", "operands": [{"$dummy": ["second", 2]}, 5]},
        ]

        assert express(list_of_dicts) == expected

    def test_with_basemodel_containing_complex_expression(self) -> None:
        """Test that express function works correctly when BaseModel expression is complex."""

        class ComplexModel(BaseModel):
            name: str = "complex"

            @property
            def expression(self) -> Expression:
                return {
                    "$complex": {
                        "name": self.name,
                        "nested": {"array": [1, 2, 3], "object": {"key": "value"}},
                    }
                }

        complex_model = ComplexModel()
        nested_structure = {
            "$pipeline": [{"$match": complex_model}, {"$group": {"_id": complex_model}}]
        }

        expected = {
            "$pipeline": [
                {
                    "$match": {
                        "$complex": {
                            "name": "complex",
                            "nested": {"array": [1, 2, 3], "object": {"key": "value"}},
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$complex": {
                                "name": "complex",
                                "nested": {
                                    "array": [1, 2, 3],
                                    "object": {"key": "value"},
                                },
                            }
                        }
                    }
                },
            ]
        }

        assert express(nested_structure) == expected

    def test_with_tuple_and_other_sequences(self) -> None:
        """Test that express function works correctly with tuples and other sequence types."""

        test_model = DummyModel()

        # Test with tuple containing BaseModel
        test_tuple = (test_model, 42, "hello")
        # Tuples should be treated as regular objects since they're immutable
        # The function should return the tuple as-is since it's not a list or dict
        assert express(test_tuple) == (test_model, 42, "hello")

        # Test with set containing BaseModel (though sets are not JSON serializable)
        # Sets should also be returned as-is
        test_set = {42, "hello"}  # Can't put BaseModel in set due to unhashable type
        assert express(test_set) == test_set
