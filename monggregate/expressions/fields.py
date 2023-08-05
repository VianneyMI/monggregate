"""Module defining field paths types"""

# Standard Library Imports
# -------------------------------------------
import re

# 3rd Party imports
# -------------------------------------------
from monggregate.base import pyd


# Types definition
# -------------------------------------------
class FieldName(pyd.ConstrainedStr):
    """Regex describing syntax for field names"""

    regex = re.compile(r"^[^\$][^\.]+$")

class FieldPath(pyd.ConstrainedStr):
    """Regex describing syntax of a field path"""

    regex = re.compile(r"^\$")

class Variable(FieldPath):
    """Regex describing reference to a variable in expressions"""

    regex = re.compile(r"^\$\$")
