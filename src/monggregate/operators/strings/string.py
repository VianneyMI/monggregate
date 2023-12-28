"""Base string operator module"""

# Standard Library Imports
# -----------------------------------------
from abc import ABC
from typing import Any

# Local imports
# -----------------------------------------
from monggregate.operators import Operator
from monggregate.utils import StrEnum

# Enums
# -----------------------------------------
class StringOperatorEnum(StrEnum):
    """Enumeration of available string operators"""

    CONCAT = "$concat" # Concatenates any number of strings.
    CONCAT_WS = "$concatWS" # Concatenates strings and returns the concatenated string.
    INDEX_OF_BYTES = "$indexOfBytes" # Searches a string for an occurence of a substring and returns the UTF-8 byte index of the first occurence. If the substring is not found, returns -1.
    INDEX_OF_CP = "$indexOfCP" # Searches a string for an occurence of a substring and returns the UTF-8 code point index of the first occurence. If the substring is not found, returns -1.
    LTRIM = "$ltrim" # Removes whitespace or the specified characters from the beginning of a string.
    REGEX_FIND = "$regexFind" # Searches a string for an occurence of a substring that matches the given regular expression pattern and returns the first occurence as a substring.
    REGEX_FIND_ALL = "$regexFindAll" # Searches a string for occurences of a substring that matches the given regular expression pattern and returns the occurences as a list of substrings.
    REGEX_MATCH = "$regexMatch" # Performs a regular expression match of a string against a pattern and returns a boolean that indicates if the pattern is found or not.
    REPLACE_ALL = "$replaceAll" # Replaces all occurences of a specified string or regular expression in a given input string with another specified string.
    REPLACE_ONE = "$replaceOne" # Replaces the first occurence of a specified string or regular expression in a given input string with another specified string.
    RTRIM = "$rtrim" # Removes whitespace or the specified characters from the end of a string.
    SPLIT = "$split" # Divides a string into substrings based on a delimiter.
    STR_LEN_BYTES = "$strLenBytes" # Returns the number of UTF-8 encoded bytes in a string.
    STR_LEN_CP = "$strLenCP" # Returns the number of UTF-8 code points in a string.
    STRCASECMP = "$strcasecmp" # Performs case-insensitive string comparison and returns: 0 if two strings are equivalent, 1 if the first string is greater than the second, and -1 if the first string is less than the second.
    SUBSTR = "$substr" # Returns the substring of a string.
    SUBSTR_BYTES = "$substrBytes" # Returns the substring of a string.



# Classes
# -----------------------------------------
class StringOperator(Operator, ABC):
    """Base class for string operators"""

# Type aliases
# -----------------------------------------
StringOperatorExpression = dict[StringOperatorEnum, Any]