"""Base accumulator module"""

from abc import ABC

from pydantic import validator

from monggregate.expressions import Expression
from monggregate.operators import Operator

class Comparator(Operator, ABC):
    """Base class for accumulators"""

    left : Expression
    right : Expression

    @validator("*", pre=True, always=True)
    @classmethod
    def convert_expressions(cls, value:Expression)->Expression|dict|None:
        """Convert expressions"""

        if isinstance(value, Comparator):
            output = value.statement
        else:
            output = value

        return output
