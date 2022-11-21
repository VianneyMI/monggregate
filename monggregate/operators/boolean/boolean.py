"""Base boolean operator module"""

from abc import ABC

from monggregate.operators import Operator

class BooleanOperator(Operator, ABC):
    """Base class for boolean operators"""