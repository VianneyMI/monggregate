import pytest
from monggregate.search.commons import FuzzyOptions, CountOptions, HighlightOptions


def test_fuzzy_options_instantiation():
    """Test that FuzzyOptions class can be instantiated correctly."""
    # Create fuzzy options with default values
    fuzzy_options = FuzzyOptions()

    # Create fuzzy options with custom values
    custom_fuzzy = FuzzyOptions(maxEdits=2, prefixLength=1, maxExpansions=50)

    # Check that the model representation works correctly
    assert custom_fuzzy.dict() == {
        "maxEdits": 2,
        "prefixLength": 1,
        "maxExpansions": 50,
    }


def test_count_options_instantiation():
    """Test that CountOptions class can be instantiated correctly."""
    # Create count options
    count_options = CountOptions(type="total")

    # Check the representation
    assert count_options.dict() == {"type": "total"}
