"""Tests for the Skip stage."""

from monggregate.stages import Skip


class TestSkip:
    """Tests for the Skip stage."""

    def test_instantiation(self) -> None:
        """Test that the Skip stage can be instantiated correctly."""

        skip = Skip(value=10)
        assert isinstance(skip, Skip)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        skip = Skip(value=10)
        assert skip.expression == {"$skip": 10}
