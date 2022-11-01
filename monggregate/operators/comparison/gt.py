"""xxx"""

from pydantic import validator
from monggregate.expressions import Expression
from monggregate.operators.comparison.comparator import Comparator

class GreatherThan(Comparator):
    """xxxx"""

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