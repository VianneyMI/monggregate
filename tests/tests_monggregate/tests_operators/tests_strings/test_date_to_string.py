"""Tests for `monggregate.operators.strings.date_to_string` module."""

from monggregate.operators.strings.date_to_string import DateToString

def test_date_to_string_expression_full():
    # Setup
    date = "$date"
    format_ = "%Y-%m-%d"
    timezone = "America/New_York"
    on_null = "No date available"
    expected_expression = {
        "$dateToString": {
            "date": "$date",
            "format": "%Y-%m-%d",
            "timezone": "America/New_York",
            "onNull": "No date available",
        }
    }

    # Act
    date_to_string_op = DateToString(
        date=date,
        format_=format_,
        timezone=timezone,
        on_null=on_null,
    )
    result_expression = date_to_string_op.expression

    # Assert
    assert result_expression == expected_expression


class TestDateToString:
    """Tests for `DateToString` class."""

    def test_instantiation_minimal(self) -> None:
        """Test that `DateToString` class can be instantiated with minimal parameters."""
        date_to_string_op = DateToString(
            date="$date", format_=None, timezone=None, on_null=None
        )
        assert isinstance(date_to_string_op, DateToString)

    def test_instantiation_full(self) -> None:
        """Test that `DateToString` class can be instantiated with all parameters."""
        date_to_string_op = DateToString(
            date="$date",
            format_="%Y-%m-%d",
            timezone="America/New_York",
            on_null="No date available",
        )
        assert isinstance(date_to_string_op, DateToString)

    def test_expression_minimal(self) -> None:
        """Test that `DateToString` class returns the correct expression with minimal parameters."""
        date_to_string_op = DateToString(
            date="$date", format_=None, timezone=None, on_null=None
        )
        assert date_to_string_op.expression == {"$dateToString": {"date": "$date"}}

    def test_expression_full(self) -> None:
        """Test that `DateToString` class returns the correct expression with all parameters."""
        date_to_string_op = DateToString(
            date="$date",
            format_="%Y-%m-%d",
            timezone="America/New_York",
            on_null="No date available",
        )
        assert date_to_string_op.expression == {
            "$dateToString": {
                "date": "$date",
                "format": "%Y-%m-%d",
                "timezone": "America/New_York",
                "onNull": "No date available",
            }
        }
