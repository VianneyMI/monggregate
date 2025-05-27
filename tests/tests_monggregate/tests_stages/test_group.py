"""Tests for the Group stage."""

from monggregate.stages import Group


class TestGroup:
    """Tests for the Group stage."""

    def test_instantiation(self) -> None:
        """Test that the Group stage can be instantiated."""
        group = Group(by="field")
        assert isinstance(group, Group)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        group = Group(by="field")
        assert group.expression == {"$group": {"_id": "$field"}}

    def test_expression_with_query(self) -> None:
        """Test that the query parameter is validated."""

        group = Group(by="field", query={"count": {"$sum": 1}})
        # fmt: off
        assert group.expression == {
            "$group": {
                "_id": "$field", 
                "count": {"$sum": 1}
                }
        }
        # fmt: on
