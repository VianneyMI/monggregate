"""Tests for the Stage class."""

import pytest
from monggregate.base import Expression
from monggregate.stages import Stage


class TestStage:
    """Tests for the Stage class."""

    def test_is_abstract(self) -> None:
        """Test that the Stage class is abstract."""

        with pytest.raises(TypeError):
            Stage()

    def test_wrong_subclassing(self) -> None:
        """Test that the Stage class can be subclassed."""

        class DummyStage(Stage):
            """Dummy subclass of Stage."""

        assert issubclass(DummyStage, Stage)

        with pytest.raises(TypeError):
            dummy_stage = DummyStage()

    def test_good_subclassing(self) -> None:
        """Test that the Stage class can be subclassed."""

        class DummyStage(Stage):
            """Dummy subclass of Stage."""

            @property
            def expression(self) -> Expression:
                """Return the expression for the stage."""

                return {"$dummy": 1}

        dummy_stage = DummyStage()
        assert dummy_stage.expression == {"$dummy": 1}
