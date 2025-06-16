"""Test utilities for monggregate tests."""


def generate_enum_member_name(value: str) -> str:
    """Generate the expected enum member name from a value.

    Args:
        value: The enum value (with or without $ prefix)

    Returns:
        The expected member name in UPPER_SNAKE_CASE format

    Example:
        >>> generate_enum_member_name("$addToSet")
        'ADD_TO_SET'
        >>> generate_enum_member_name("bottomN")
        'BOTTOM_N'
    """
    # Remove the $ prefix if present
    value_name = value[1:] if value.startswith("$") else value

    # Handle empty string case
    if not value_name:
        return ""

    # Split camelCase into words, keeping consecutive uppercase letters together
    words = []
    current_word = ""
    i = 0

    while i < len(value_name):
        char = value_name[i]

        if char.isupper():
            # If current word has lowercase letters, start a new word
            if current_word and current_word[-1].islower():
                words.append(current_word)
                current_word = char
            else:
                # Check if this is part of a consecutive uppercase sequence
                # Look ahead to see if next char is lowercase (indicating end of acronym)
                if (
                    i + 1 < len(value_name)
                    and value_name[i + 1].islower()
                    and current_word
                    and current_word[-1].isupper()
                ):
                    # This uppercase letter starts a new word (like 'C' in 'CP' when followed by lowercase)
                    words.append(current_word)
                    current_word = char
                else:
                    # Continue the current word
                    current_word += char
        else:
            # Lowercase letter - continue current word
            current_word += char

        i += 1

    if current_word:
        words.append(current_word)

    # Convert to UPPER_SNAKE_CASE
    return "_".join(word.upper() for word in words)


class TestGenerateEnumMemberName:
    """Tests for the `generate_enum_member_name` function."""

    def test_with_real_operator_names(self) -> None:
        """Test that the `generate_enum_member_name` function generates the correct enum member name."""

        assert generate_enum_member_name("$addToSet") == "ADD_TO_SET"
        assert generate_enum_member_name("bottomN") == "BOTTOM_N"
        assert generate_enum_member_name("topN") == "TOP_N"
        assert generate_enum_member_name("bottomN") == "BOTTOM_N"

    def test_with_stages_names(self) -> None:
        """Test that the `generate_enum_member_name` function generates the correct enum member name."""

        assert generate_enum_member_name("$lookup") == "LOOKUP"
        assert generate_enum_member_name("$project") == "PROJECT"
        assert generate_enum_member_name("$match") == "MATCH"
        assert generate_enum_member_name("$unwind") == "UNWIND"
        assert generate_enum_member_name("$group") == "GROUP"
        assert generate_enum_member_name("$sort") == "SORT"
        assert generate_enum_member_name("$limit") == "LIMIT"
        assert generate_enum_member_name("$skip") == "SKIP"
        assert generate_enum_member_name("$sample") == "SAMPLE"

    def test_on_random_names(self) -> None:
        """Test that the `generate_enum_member_name` function generates the correct enum member name."""

        assert generate_enum_member_name("random_name") == "RANDOM_NAME"
        assert generate_enum_member_name("addToSet") == "ADD_TO_SET"

    def test_consecutive_uppercase_letters(self) -> None:
        """Test that consecutive uppercase letters are kept together."""

        # These are the problematic cases that currently fail
        assert generate_enum_member_name("$indexOfCP") == "INDEX_OF_CP"
        assert generate_enum_member_name("$indexCP") == "INDEX_CP"
        assert generate_enum_member_name("$strLenCP") == "STR_LEN_CP"
        assert generate_enum_member_name("$indexOfBytes") == "INDEX_OF_BYTES"
        assert generate_enum_member_name("$substrCP") == "SUBSTR_CP"
        assert generate_enum_member_name("$strLenBytes") == "STR_LEN_BYTES"
        assert generate_enum_member_name("$substrBytes") == "SUBSTR_BYTES"

    def test_edge_cases(self) -> None:
        """Test that the `generate_enum_member_name` function generates the correct enum member name on edge cases.

        - Empty string
        - Single letter
        - Single letter with $ prefix
        - Single letter without $ prefix
        - Hybrid case
        """

        assert generate_enum_member_name("") == ""
        assert generate_enum_member_name("a") == "A"
        assert generate_enum_member_name("$a") == "A"
        assert generate_enum_member_name("aB") == "A_B"
        assert generate_enum_member_name("aBc") == "A_BC"
        assert generate_enum_member_name("XMLHttpRequest") == "XML_HTTP_REQUEST"
        assert generate_enum_member_name("HTMLParser") == "HTML_PARSER"
        assert generate_enum_member_name("JSONData") == "JSON_DATA"
