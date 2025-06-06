"""Tests for `monggregate.operators.strings.date_from_string` module."""

from monggregate.operators.strings.date_from_string import DateFromString

def test_date_from_string_expression_full():
    # Setup
    date_string = "2023-01-01"
    format_ = "%Y-%m-%d"
    timezone = "America/New_York"
    on_error = "Invalid date"
    on_null = "No date provided"
    expected_expression = {
        "$dateFromString": {
            "dateString": "2023-01-01",
            "format": "%Y-%m-%d",
            "timezone": "America/New_York",
            "onError": "Invalid date",
            "onNull": "No date provided",
        }
    }

    # Act
    date_from_string_op = DateFromString(
        date_string=date_string,
        format_=format_,
        timezone=timezone,
        on_error=on_error,
        on_null=on_null,
    )
    result_expression = date_from_string_op.expression

    # Assert
    assert result_expression == expected_expression


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
