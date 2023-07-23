"""Module defining field paths types"""

# Standard Library Imports
# -------------------------------------------
import re

# 3rd Party imports
# -------------------------------------------
import pydantic
if pydantic.__version__.startswith("1"):
    from pydantic import ConstrainedStr
else:
    from pydantic.v1.types import ConstrainedStr

# Types definition
# -------------------------------------------
class FieldName(ConstrainedStr):
    """Regex describing syntax for field names"""

    regex = re.compile(r"^[^\$][^\.]+$")

class FieldPath(ConstrainedStr):
    """Regex describing syntax of a field path"""

    regex = re.compile(r"^\$")

class Variable(FieldPath):
    """Regex describing reference to a variable in expressions"""

    regex = re.compile(r"^\$\$")
