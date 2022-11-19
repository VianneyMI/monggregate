"""Base array operator module"""

from abc import ABC

from monggregate.expressions import Expression
from monggregate.operators import Operator

class ArrayOperator(Operator, ABC):
    """Base class for array operators"""



class ArrayOnlyOperator(ArrayOperator, ABC):
    """Base class for array operators that work directly on the input array without any other parameters"""

    expression : Expression
