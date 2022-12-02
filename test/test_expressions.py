
"""Module to test expressions"""


import pytest
from pydantic import BaseModel, Field, ValidationError
from pydantic.errors import StrRegexError
from monggregate.stages.count import FieldName


def test_constraints_in_hybrid_types()->None:
    """
    Testes pydantic constraints on Union types

    Ensures that constraints are taken into account for Union types, only for the relevant type of the Union.
    """

    class Test(BaseModel):
        """Test class with hybrid type"""

        x : int | dict = Field(gt=1)

    assert Test(x=2)
    assert Test(x={})
    with pytest.raises(ValidationError):
        assert Test(x=0)

def test_field_name()->None:
    """Testes the FieldName regex"""

    assert FieldName.validate("good_name")

    assert FieldName.validate("thisIs$good")
    with pytest.raises(StrRegexError):
        FieldName.validate("this.contains_a_dot")

    with pytest.raises(StrRegexError):
        FieldName.validate("$Startwith$")

if __name__=="__main__":
    test_constraints_in_hybrid_types()
    test_field_name()
    print("ok")