"""Base object operator module"""

from abc import ABC

from monggregate.operators import Operator

class ObjectOperator(Operator, ABC):
    """Base class for object operators"""