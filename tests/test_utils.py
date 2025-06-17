"""Tests for the `tests.utils` module."""

from tests.utils import generate_enum_member_name


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
