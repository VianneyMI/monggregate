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

    # Split camelCase into words
    words = []
    current_word = value_name[0]

    for char in value_name[1:]:
        if char.isupper():
            words.append(current_word)
            current_word = char
        else:
            current_word += char

    words.append(current_word)

    # Convert to UPPER_SNAKE_CASE
    return "_".join(word.upper() for word in words)
