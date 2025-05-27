"""Tests for the Project stage."""

import pytest
from monggregate.stages import Project


class TestProject:
    """Tests for the Project stage."""

    def test_instantiation(self) -> None:
        """Test that the Project stage can be instantiated correctly."""

        project = Project(projection={"field1": 1, "field2": 1})
        assert isinstance(project, Project)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        project = Project(projection={"field1": 1, "field2": 1})
        assert project.expression == {"$project": {"field1": 1, "field2": 1}}

    def test_expression_with_include_as_list_of_strings(self) -> None:
        """Test that the expression method returns the correct expression with include."""

        project = Project(include=["field1", "field2"])
        assert project.expression == {"$project": {"field1": 1, "field2": 1}}

    def test_expression_with_include_as_dict(self) -> None:
        """Test that the expression method returns the correct expression with include."""

        project = Project(include={"field1": 1, "field2": 1})
        assert project.expression == {"$project": {"field1": 1, "field2": 1}}

    def test_expression_with_include_as_bool(self) -> None:
        """Test that the expression method returns the correct expression with include."""

        project = Project(include=True, fields=["field1", "field2"])
        assert project.expression == {"$project": {"field1": 1, "field2": 1}}

    def test_expression_with_exclude_as_list_of_strings(self) -> None:
        """Test that the expression method returns the correct expression with exclude."""

        project = Project(exclude=["field1", "field2"])
        assert project.expression == {"$project": {"field1": 0, "field2": 0}}

    def test_expression_with_exclude_as_dict(self) -> None:
        """Test that the expression method returns the correct expression with exclude."""

        project = Project(exclude={"field1": 0, "field2": 0})
        assert project.expression == {"$project": {"field1": 0, "field2": 0}}

    @pytest.mark.xfail(reason="Bug in the code.")
    # NOTE: The issue is that when using booleans, only include is used.
    # We should find a mechanism so that include = !exclude and vice versa.
    # Or review the logic of the code.
    def test_expression_with_exclude_as_bool(self) -> None:
        """Test that the expression method returns the correct expression with exclude."""

        project = Project(exclude=True, fields=["field1", "field2"])
        assert project.expression == {"$project": {"field1": 0, "field2": 0}}

    def test_expression_with_include_and_exclude_both_as_list_of_strings(self) -> None:
        """Test that the expression method returns the correct expression with include and exclude."""

        project = Project(include=["field1", "field2"], exclude=["field3", "field4"])
        assert project.expression == {
            "$project": {"field1": 1, "field2": 1, "field3": 0, "field4": 0}
        }

    @pytest.mark.xfail(reason="Bug in the code.")
    # NOTE: The issue is that when using booleans, only include is used.
    # We should find a mechanism so that include = !exclude and vice versa.
    # Or review the logic of the code.
    def test_expression_with_include_and_exclude_both_as_dict(self) -> None:
        """Test that the expression method returns the correct expression with include and exclude."""

        project = Project(
            include={"field1": 1, "field2": 1}, exclude={"field3": 1, "field4": 1}
        )
        assert project.expression == {
            "$project": {"field1": 1, "field2": 1, "field3": 0, "field4": 0}
        }

    def test_expression_with_include_and_exclude_both_as_bool(self) -> None:
        """Test that the expression method returns the correct expression with include and exclude."""

        # NOTE: This should raise a ValueError
        with pytest.raises(ValueError):
            project = Project(include=True, exclude=True, fields=["field1", "field2"])

    @pytest.mark.xfail(reason="This fails but we might want to forbid this case.")
    def test_expression_with_include_and_exclude_both_as_bool_and_list_of_strings(
        self,
    ) -> None:
        """Test that the expression method returns the correct expression with include and exclude."""

        project = Project(
            include=True, exclude=["field3", "field4"], fields=["field1", "field2"]
        )
        assert project.expression == {
            "$project": {"field1": 1, "field2": 1, "field3": 0, "field4": 0}
        }
