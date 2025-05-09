import pytest
from monggregate.dollar import (
    AggregationVariableEnum,
    Dollar,
    DollarDollar,
    CLUSTER_TIME,
    NOW,
    ROOT,
    CURRENT,
    REMOVE,
    DESCEND,
    PRUNE,
    KEEP,
    CONSTANTS,
    S,
    SS,
)


class TestAggregationVariableEnum:
    """Tests consistency of the `AggregationVariableEnum` class."""

    def test_members_consistency(self):
        """Tests consistency betweew the keys and the values of the enum."""

    # Iterate over the members of the enum
    checks = []
    wrong_members = []

    for key, value in AggregationVariableEnum.__members__.items():
        if key == value.value.replace("$$", ""):
            checks.append(True)
        else:
            checks.append(False)
            wrong_members.append((key, value.value))

    assert all(checks), f"The following members are not consistent: {wrong_members}"

    def test_constants_consistency(self):
        """Tests consistency of the constants in the `dollar` module."""

        # assert len(CONSTANTS) == len(AggregationVariableEnum.__members__)

        checks_constants_in_enum = []
        checks_enum_in_constants = []
        missing_constants_in_enum = []
        missing_enum_in_constants = []

        for constant in CONSTANTS:
            if constant in AggregationVariableEnum.__members__.values():
                checks_constants_in_enum.append(True)
            else:
                checks_constants_in_enum.append(False)
                missing_constants_in_enum.append(constant)

        for enum in AggregationVariableEnum.__members__.values():
            if enum.value in CONSTANTS:
                checks_enum_in_constants.append(True)
            else:
                checks_enum_in_constants.append(False)
                missing_enum_in_constants.append(enum.value)

        error_message = "Inconsistency between the constants and the enum: \n"
        if missing_constants_in_enum:
            error_message += f"  * The following constants are not in the enum: {missing_constants_in_enum}\n"
        if missing_enum_in_constants:
            error_message += f"  * The following enum values are not in the constants: {missing_enum_in_constants}\n"

        assert all(checks_constants_in_enum) and all(checks_enum_in_constants), (
            error_message
        )


class TestDollar:
    """Test the Dollar class."""

    def test_instantiation(self):
        """Test that Dollar class can be accessed correctly and returns dollar-prefixed fields."""

        dollar = Dollar()
        assert isinstance(dollar, Dollar)

    def test_singleton(self):
        """Test that Dollar class is a singleton."""

        assert Dollar() is Dollar()
        assert Dollar() is S

    def test____getattr__(self):
        """Test the __getattr__ method of the Dollar class."""

        # Test field reference
        assert Dollar().name == "$name"

    def test_field(self):
        """Test the field() method of the Dollar class."""

        # Test field() method
        assert Dollar().field("price") == "$price"

    # -----------------------------------
    # Add tests for the other methods
    # -----------------------------------

    # .......


class TestDollarDollar:
    """Test the DollarDollar class."""

    def test_instantiation(self):
        """Test that DollarDollar class can be accessed correctly and returns dollar-prefixed fields."""

        dollar_dollar = DollarDollar()
        assert isinstance(dollar_dollar, DollarDollar)

    def test____getattr__(self):
        """Test the __getattr__ method of the DollarDollar class."""

        assert DollarDollar().name == "$$name"
