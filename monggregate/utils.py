""""Utilities"""

# Standard Library Imports
# ------------------------------
from typing import TypeVar
from enum import Enum

# Typing
#------------------------------
T =  TypeVar("T")

# Classes
# ------------------------------
class StrEnum(str, Enum):
    """Base Class for string enums"""

    def __str__(self)->str:
        """Returns the value of the enum"""
        return self.value

# Functions
#-------------------------------
def _to_unique_list(keys:str|list[str]|set[str])->list[str]:
    """
    Returns a list of unique keys from the provided key(s)

    Raises
    -------------------------------------------
        - TypeError, is keys is neither a str, list[str] or set[str]

    """

    # Case 1 : keys is a set
    # ----------------------
    if isinstance(keys, set):
        output = list(keys) # we just have to transform it to a list

    # Case 2 : keys is a str
    # ------------------------
    elif isinstance(keys, str):
        output = [keys] # we just have to transform it to a list of
                        # a single element

    # Case 3 : keys is a list
    # ---------------------------
    elif isinstance(keys, list):
        output = list(set(keys)) # we need to transform it
                                 # to a set to ensure uniqueness
                                 # then to convert it back to a list
    else:
        raise TypeError(f"keys should be either a of type str, list[str] or set[str]. Got type {type(keys)} instead")

    return output

# TODO : Fix typing using overload <VM, 26/10/2022>
def to_unique_list(keys:T)->list[str]|T:
    """Returns a list of unique keys from the provided key(s) if keys is valid or returns keys if keys is not valid"""

    try:
        output = _to_unique_list(keys) # type: ignore[arg-type]
    except TypeError:
        output = keys # type: ignore[assignment]

    return output

def validate_field_path(path:str|None)->str|None:
    """Validates field path"""

    if isinstance(path, str) and not path.startswith("$"):
        path =  "$" + path

    return path


def validate_field_paths(paths:list[str]|set[str])->list[str]:
    """Validates field paths"""

    if isinstance(paths, list):
        paths = [validate_field_path(path) for path in paths]
    elif isinstance(paths, set):
        paths = [validate_field_path(path) for path in paths]
        paths.sort()

    return paths
