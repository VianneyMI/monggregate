"""Base accumulator module"""

from abc import ABC

from pydantic import validator

from monggregate.expressions import Expression
from monggregate.operators import Operator

class ArrayOperator(Operator, ABC):
    """Base class for accumulators"""

    expression : Expression

