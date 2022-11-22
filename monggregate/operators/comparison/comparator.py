"""Base accumulator module"""

from abc import ABC

from pydantic import validator

from typing import Any
from monggregate.operators import Operator

class Comparator(Operator, ABC):
    """Base class for accumulators"""

    left : Any
    right : Any

