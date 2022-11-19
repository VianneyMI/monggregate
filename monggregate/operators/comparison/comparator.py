"""Base accumulator module"""

from abc import ABC

from pydantic import validator

from monggregate.expressions import Expression
from monggregate.operators import Operator

class Comparator(Operator, ABC):
    """Base class for accumulators"""

    left : Expression
    right : Expression

