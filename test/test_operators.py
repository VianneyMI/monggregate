"""
Module unit testing the stages.

Checks that at least each stage can be instantiated properly.

"""

import pytest
from pydantic import ValidationError

from monggregate.operators import( # pylint: disable=import-error
    And,
    Sum,
    Filter,
    First
)

# ----------------------
# Units Tests
# ----------------------
@pytest.mark.unit
def test_()->None:
    """
    Test template.

    Copy/Paste me to create new tests
    """

    # Testing mandatory attributes
    # -----------------------------


    # Testing aliases
    # -----------------------------


    # Testing optional attributes
    # -----------------------------
@pytest.mark.latest
@pytest.mark.unit
def test_and()->None:
    """Testes and operator"""

    and_operator =  And(
        expressions=[
            First(expression=[1, 2, 3, 4]),
            First(expression=[4, 5, 6, 7])
        ]
    )

    assert and_operator
    print(and_operator.statement)
    assert and_operator.statement == {
        "$and" : [
            {
                "$first" : [1, 2, 3, 4]
            },
            {
                "$first" : [4, 5, 6, 7]
            }
        ]
    }

if __name__ == "__main__":
    test_and()
