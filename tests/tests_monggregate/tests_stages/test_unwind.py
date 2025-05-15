"""Tests for the Unwind stage."""

import pytest
from monggregate.stages import Unwind


class TestUnwind:
    """Tests for the Unwind stage."""

    def test_instantiation(self) -> None:
        """Test that the Unwind stage can be instantiated."""

        unwind = Unwind(path_to_array="field")
        assert isinstance(unwind, Unwind)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        unwind = Unwind(path_to_array="field")
        assert unwind.expression == {"$unwind": {"path": "$field"}}

    def test_expression_with_include_array_index(self) -> None:
        """Test that the expression method returns the correct expression with include_array_index."""

        unwind = Unwind(path_to_array="field", include_array_index="index")
        assert unwind.expression == {
            "$unwind": {"path": "$field", "includeArrayIndex": "index"}
        }

    def test_expression_with_always(self) -> None:
        """Test that the expression method returns the correct expression with always."""

        unwind = Unwind(path_to_array="field", always=True)
        assert unwind.expression == {
            "$unwind": {"path": "$field", "preserveNullAndEmptyArrays": True}
        }
