"""Test utilities for monggregate tests."""


def _remove_dollar_prefix(value: str) -> str:
    """Remove the $ prefix from a value if present.

    Args:
        value: The enum value that may have a $ prefix

    Returns:
        The value without the $ prefix
    """
    return value[1:] if value.startswith("$") else value


def _should_start_new_word_after_uppercase(
    current_word: str, current_index: int, value_name: str
) -> bool:
    """Determine if we should start a new word after encountering an uppercase letter.

    Args:
        current_word: The current word being built
        current_index: Current position in the string
        value_name: The full string being processed

    Returns:
        True if we should start a new word, False otherwise
    """
    if not current_word:
        return False

    # If current word ends with lowercase, start new word
    if current_word[-1].islower():
        return True

    # Check if this uppercase letter starts a new word in an acronym sequence
    # (like 'C' in 'CP' when followed by lowercase)
    next_char_is_lowercase = (
        current_index + 1 < len(value_name) and value_name[current_index + 1].islower()
    )
    current_word_ends_with_uppercase = current_word[-1].isupper()

    return next_char_is_lowercase and current_word_ends_with_uppercase


def _split_camel_case_to_words(value_name: str) -> list[str]:
    """Split a camelCase string into individual words.

    Args:
        value_name: The camelCase string to split

    Returns:
        List of words extracted from the camelCase string
    """
    words = []
    current_word = ""

    for i, char in enumerate(value_name):
        if char.isupper() and _should_start_new_word_after_uppercase(
            current_word, i, value_name
        ):
            words.append(current_word)
            current_word = char
        else:
            current_word += char

    if current_word:
        words.append(current_word)

    return words


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
    cleaned_value = _remove_dollar_prefix(value)

    # Handle empty string case by returning empty result
    words = _split_camel_case_to_words(cleaned_value) if cleaned_value else []

    enum_member_name = "_".join(word.upper() for word in words)
    return enum_member_name
