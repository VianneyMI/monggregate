"""Tests for `monggregate.operators.strings.date_from_string` module."""

from monggregate.operators.strings.date_from_string import DateFromString


class TestDateFromString:
    """Tests for `DateFromString` class."""

    def test_instantiation_minimal(self) -> None:
        """Test that `DateFromString` class can be instantiated with minimal parameters."""
        date_from_string_op = DateFromString(
            date_string="2023-01-01",
            format_=None,
            timezone=None,
            on_error=None,
            on_null=None,
        )
        assert isinstance(date_from_string_op, DateFromString)

    def test_instantiation_full(self) -> None:
        """Test that `DateFromString` class can be instantiated with all parameters."""
        date_from_string_op = DateFromString(
            date_string="2023-01-01",
            format_="%Y-%m-%d",
            timezone="America/New_York",
            on_error="Invalid date",
            on_null="No date provided",
        )
        assert isinstance(date_from_string_op, DateFromString)

    def test_expression_minimal(self) -> None:
        """Test that `DateFromString` class returns the correct expression with minimal parameters."""
        date_from_string_op = DateFromString(
            date_string="2023-01-01",
            format_=None,
            timezone=None,
            on_error=None,
            on_null=None,
        )
        assert date_from_string_op.expression == {
            "$dateFromString": {"dateString": "2023-01-01"}
        }

    def test_expression_full(self) -> None:
        """Test that `DateFromString` class returns the correct expression with all parameters."""
        date_from_string_op = DateFromString(
            date_string="2023-01-01",
            format_="%Y-%m-%d",
            timezone="America/New_York",
            on_error="Invalid date",
            on_null="No date provided",
        )
        assert date_from_string_op.expression == {
            "$dateFromString": {
                "dateString": "2023-01-01",
                "format": "%Y-%m-%d",
                "timezone": "America/New_York",
                "onError": "Invalid date",
                "onNull": "No date provided",
            }
        }
