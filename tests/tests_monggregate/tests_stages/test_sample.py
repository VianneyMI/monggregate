"""Tests for the Sample stage."""

from monggregate.stages import Sample


class TestSample:
    """Tests for the Sample stage."""

    def test_instantiation(self) -> None:
        """Test that the Sample stage can be instantiated correctly."""

        sample = Sample(value=10)
        assert isinstance(sample, Sample)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        sample = Sample(value=10)
        assert sample.expression == {"$sample": {"size": 10}}
