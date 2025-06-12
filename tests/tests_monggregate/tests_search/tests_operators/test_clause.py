from monggregate.search.operators.autocomplete import Autocomplete
from monggregate.search.operators.equals import Equals
from monggregate.search.operators.exists import Exists
from monggregate.search.operators.more_like_this import MoreLikeThis
from monggregate.search.operators.range import Range
from monggregate.search.operators.regex import Regex
from monggregate.search.operators.text import Text
from monggregate.search.operators.wildcard import Wildcard

from src.monggregate.search.operators.clause import Clause


def test_clause_union_type():
    # Setup
    autocomplete = Autocomplete(query="test", path="field")
    equals = Equals(path="field", value="value")
    exists = Exists(path="field")
    more_like_this = MoreLikeThis(like="example")
    range_op = Range(path="field", gte=1, lte=10)
    regex = Regex(path="field", query="^abc")
    text = Text(query="something", path="field")
    wildcard = Wildcard(path="field", query="a*")

    # Act & Assert
    assert isinstance(autocomplete, Clause)
    assert isinstance(equals, Clause)
    assert isinstance(exists, Clause)
    assert isinstance(more_like_this, Clause)
    assert isinstance(range_op, Clause)
    assert isinstance(regex, Clause)
    assert isinstance(text, Clause)
    assert isinstance(wildcard, Clause)

class TestClause:
    """Tests for `Clause` union type."""

    def test_autocomplete_is_clause(self):
        assert isinstance(Autocomplete(query="x", path="field"), Clause)

    def test_equals_is_clause(self):
        assert isinstance(Equals(path="field", value="v"), Clause)

    def test_exists_is_clause(self):
        assert isinstance(Exists(path="field"), Clause)

    def test_more_like_this_is_clause(self):
        assert isinstance(MoreLikeThis(like="sample"), Clause)

    def test_range_is_clause(self):
        assert isinstance(Range(path="field", gte=1), Clause)

    def test_regex_is_clause(self):
        assert isinstance(Regex(path="field", query="abc"), Clause)

    def test_text_is_clause(self):
        assert isinstance(Text(query="some", path="field"), Clause)

    def test_wildcard_is_clause(self):
        assert isinstance(Wildcard(path="field", query="*a"), Clause)


# TODO
