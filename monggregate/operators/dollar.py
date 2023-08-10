"""WIP"""

from typing import Any

from monggregate.base import BaseModel

    # Avg,
    # Count,
    # First,
    # Last,
    # Max,
    # Min,
    # Push,
    # Sum
from monggregate.operators import(
    accumulators,
    array,
    comparison,
    objects,
    boolean
)
from monggregate.operators.array import(
    ArrayToObject,
    Filter,
    #First,
    In,
    IsArray,
    #Last,
    MaxN,
    MinN,
    SortArray
)
from monggregate.operators.comparison import(
    Cmp,
    Eq,
    Gt,
    Gte,
    Lt,
    Lte,
    Ne
)
from monggregate.operators.objects import(
    MergeObjects,
    ObjectToArray
)
from monggregate.operators.boolean import And, Or, Not, and_

# NOTE : If dollar is to be made to really store all of MongoDB functions i.e stages, operators and whathever they come up with
# it might de interesting to create a DollarBase class, a DollarStage class and a DollarOperator class and to use inheritance <VM, 10/08/2023>

# TODO : Do not return statement directly but rather return a class that can be used to build the statement <VM, 10/08/2023>

class Dollar(BaseModel):
    """Base class for all $ functions"""

    # Operators
    # ------------------------------

        # Accumulators
        # --------------------------
    @classmethod
    def avg(cls, expression:Any)->str:
        """Returns the $avg operator"""
        
        return accumulators.avg(expression)

    @classmethod
    def and_(cls, *args:Any)->str:
        """Returns the $and operator"""
        
        return boolean.and_(*args)
