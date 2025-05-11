import pytest
from monggregate.stages import Match


def test_match_instantiation():
    """Test that Match stage can be instantiated correctly with a simple query."""
    # Create a match stage with a simple query
    match_stage = Match(query={"status": "active"})

    # Check that the expression is correctly formatted
    assert match_stage.expression == {"$match": {"status": "active"}}

    # Test with an empty query
    empty_match = Match()
    assert empty_match.expression == {"$match": {}}

    # Test with keyword arguments
    kw_match = Match(status="completed", priority="high")
    assert kw_match.expression == {
        "$match": {"status": "completed", "priority": "high"}
    }
