"""Module defining Clause type alias."""

from monggregate.search.operators.autocomplete import Autocomplete
from monggregate.search.operators.equals import Equals
from monggregate.search.operators.exists import Exists
from monggregate.search.operators.more_like_this import MoreLikeThis
from monggregate.search.operators.range import Range
from monggregate.search.operators.regex import Regex
from monggregate.search.operators.text import Text
from monggregate.search.operators.wildcard import Wildcard

Clause = Autocomplete | Equals | Exists | MoreLikeThis | Range | Regex | Text | Wildcard
