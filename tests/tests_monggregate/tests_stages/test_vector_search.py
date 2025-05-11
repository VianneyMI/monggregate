import pytest
from monggregate.stages import VectorSearch


def test_vector_search_instantiation():
    """Test that VectorSearch stage can be instantiated correctly."""
    # Test with basic configuration
    vector_search_stage = VectorSearch(
        index="product_vectors",
        path="description_vector",
        query_vector=[0.1, 0.2, 0.3, 0.4, 0.5],
        num_candidates=100,
        limit=10,
        filter=None,
    )

    expected_expression = {
        "$vectorSearch": {
            "index": "product_vectors",
            "path": "description_vector",
            "queryVector": [0.1, 0.2, 0.3, 0.4, 0.5],
            "numCandidates": 100,
            "limit": 10,
            "filter": None,
        }
    }

    assert vector_search_stage.expression == expected_expression

    # Test with filter
    vector_search_stage2 = VectorSearch(
        index="user_embeddings",
        path="profile_vector",
        query_vector=[0.2, 0.3, 0.4, 0.5, 0.6],
        num_candidates=50,
        limit=5,
        filter={"category": "electronics", "price": {"$lt": 1000}},
    )

    expected_expression2 = {
        "$vectorSearch": {
            "index": "user_embeddings",
            "path": "profile_vector",
            "queryVector": [0.2, 0.3, 0.4, 0.5, 0.6],
            "numCandidates": 50,
            "limit": 5,
            "filter": {"category": "electronics", "price": {"$lt": 1000}},
        }
    }

    assert vector_search_stage2.expression == expected_expression2


def test_vector_search_validation():
    """Test that VectorSearch validates inputs correctly."""
    # Test that num_candidates must be greater than limit
    with pytest.raises(ValueError):
        VectorSearch(
            index="test_index",
            path="vector_field",
            query_vector=[0.1, 0.2, 0.3],
            num_candidates=5,  # Less than limit
            limit=10,
            filter=None,
        )
