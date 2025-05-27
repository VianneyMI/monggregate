import pytest
from monggregate.stages import VectorSearch


class TestVectorSearch:
    """Tests for the VectorSearch stage."""

    def test_instantiation(self) -> None:
        """Test that the VectorSearch stage can be instantiated."""

        vector_search = VectorSearch(
            index="index",
            path="field",
            query_vector=[1, 2, 3],
            num_candidates=11,
            limit=10,
        )
        assert isinstance(vector_search, VectorSearch)

    def test_validate_num_candidates(self) -> None:
        """Test that the num_candidates is less than or equal to the limit."""

        limit = 10

        with pytest.raises(ValueError):
            VectorSearch(
                index="index",
                path="field",
                query_vector=[1, 2, 3],
                num_candidates=limit,
                limit=limit,
            )

        with pytest.raises(ValueError):
            VectorSearch(
                index="index",
                path="field",
                query_vector=[1, 2, 3],
                num_candidates=limit - 1,
                limit=limit,
            )

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        vector_search = VectorSearch(
            index="index",
            path="field",
            query_vector=[1, 2, 3],
            num_candidates=11,
            limit=10,
        )
        assert vector_search.expression == {
            "$vectorSearch": {
                "index": "index",
                "path": "field",
                "queryVector": [1, 2, 3],
                "numCandidates": 11,
                "limit": 10,
                "filter": None,
            }
        }
