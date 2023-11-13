"""Module to test expressions"""


import pytest
import pydantic
from monggregate.base import pyd
from monggregate.fields import FieldName



def test_constraints_in_hybrid_types()->None:
    """
    Tests pydantic constraints on Union types

    Ensures that constraints are taken into account for Union types, only for the relevant type of the Union.
    """

    class Test(pyd.BaseModel):
        """Test class with hybrid type"""

        x : int | dict = pyd.Field(gt=1)

    assert Test(x=2)
    assert Test(x={})
    with pytest.raises(pyd.ValidationError):
        assert Test(x=0)

def test_field_name()->None:
    """Tests the FieldName regex"""

    assert FieldName.validate("good_name")

    assert FieldName.validate("thisIs$good")
    with pytest.raises(pyd.errors.StrRegexError):
        FieldName.validate("this.contains_a_dot")

    with pytest.raises(pyd.errors.StrRegexError):
        FieldName.validate("$Startwith$")

if __name__=="__main__":
    test_constraints_in_hybrid_types()
    test_field_name()
    print("ok")