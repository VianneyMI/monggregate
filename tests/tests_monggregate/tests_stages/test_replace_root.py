"""Tests for the ReplaceRoot stage."""

from monggregate.stages import ReplaceRoot


class TestReplaceRoot:
    """Tests for the ReplaceRoot stage."""

    def test_instantiation(self) -> None:
        """Test that the ReplaceRoot stage can be instantiated correctly."""

        replace_root = ReplaceRoot(path_to_new_root="field1", document={"field2": 1})
        assert isinstance(replace_root, ReplaceRoot)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        replace_root = ReplaceRoot(path_to_new_root="field1")
        assert replace_root.expression == {"$replaceRoot": {"newRoot": "$field1"}}

    def test_expression_with_document(self) -> None:
        """Test that the expression method returns the correct expression with path_to_new_root."""

        replace_root = ReplaceRoot(
            document={
                "$mergeObjects": [{"_id": "$_id", "first": "", "last": ""}, "$name"]
            }
        )
        assert replace_root.expression == {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [{"_id": "$_id", "first": "", "last": ""}, "$name"]
                }
            }
        }
