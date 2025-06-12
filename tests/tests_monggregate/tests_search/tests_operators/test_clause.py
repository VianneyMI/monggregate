import pytest
from monggregate.search.operators.autocomplete import Autocomplete
from monggregate.search.operators.equals import Equals
from monggregate.search.operators.exists import Exists
from monggregate.search.operators.more_like_this import MoreLikeThis
from monggregate.search.operators.range import Range
from monggregate.search.operators.regex import Regex
from monggregate.search.operators.text import Text
from monggregate.search.operators.wildcard import Wildcard

class TestSearchOperators:
    """Tests unitaires pour tous les opérateurs de recherche de monggregate."""

    def test_autocomplete(self):
        """Teste la génération de l'expression autocomplete."""
        autocomplete = Autocomplete(query="test", path="field")
        expected = {"autocomplete": {"query": "test", "path": "field"}}
        assert autocomplete.expression == expected

    def test_equals(self):
        """Teste la génération de l'expression equals."""
        equals = Equals(value=42, path="field")
        expected = {"equals": {"value": 42, "path": "field"}}
        assert equals.expression == expected

    def test_exists(self):
        """Teste la génération de l'expression exists."""
        exists = Exists(path="field")
        expected = {"exists": {"path": "field"}}
        assert exists.expression == expected

    def test_more_like_this(self):
        """Teste la génération de l'expression moreLikeThis."""
        more_like_this = MoreLikeThis(like="test", path="field")
        expected = {"moreLikeThis": {"like": "test", "path": "field"}}
        assert more_like_this.expression == expected

    def test_range(self):
        """Teste la génération de l'expression range."""
        range_op = Range(path="field", gt=10, lt=20)
        expected = {"range": {"path": "field", "gt": 10, "lt": 20}}
        assert range_op.expression == expected

    def test_regex(self):
        """Teste la génération de l'expression regex."""
        regex = Regex(pattern="^test", path="field")
        expected = {"regex": {"pattern": "^test", "path": "field"}}
        assert regex.expression == expected

    def test_text(self):
        """Teste la génération de l'expression text."""
        text = Text(query="test", path="field")
        expected = {"text": {"query": "test", "path": "field"}}
        assert text.expression == expected

    def test_wildcard(self):
        """Teste la génération de l'expression wildcard."""
        wildcard = Wildcard(query="test", path="field")
        expected = {"wildcard": {"query": "test", "path": "field"}}
        assert wildcard.expression == expected



# TODO
