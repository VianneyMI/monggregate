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

# Variables. Accessed as a string with a $$ prefix followed by the fixed name and falling into three sub-categories:

    # Context System Variables. 

        # With values coming from the system environment rather than each input record an aggregation stage is processing.  
        # Examples: "$$NOW", "$$CLUSTER_TIME"

    # Marker Flag System Variables. 

        # To indicate desired behaviour to pass back to the aggregation runtime.  
        # Examples: "$$ROOT", "$$REMOVE", "$$PRUNE"

    # Bind User Variables. 

        # For storing values you declare with a $let operator (or with the let option of a $lookup stage, or as option of a $map or $filter stage).  
        # Examples: "$$product_name_var", "$$orderIdVal"