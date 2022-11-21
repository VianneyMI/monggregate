"""Base accumulator module"""

from abc import ABC

from monggregate.operators import Operator

class Accumulator(Operator, ABC):
    """Base class for accumulators"""
