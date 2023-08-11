"""WIP"""

from typing import Any, Literal

from monggregate.base import BaseModel

from monggregate.operators import(
    accumulators,
    array,
    comparison,
    objects,
    boolean
)

# NOTE : If dollar is to be made to really store all of MongoDB functions i.e stages, operators and whathever they come up with
# it might de interesting to create a DollarBase class, a DollarStage class and a DollarOperator class and to use inheritance <VM, 10/08/2023>

# TODO : Do not return statement directly but rather return a class that can be used to build the statement <VM, 10/08/2023>
# TODO : Fix return types
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
    def count(cls)->str:
        """Returns the $count operator"""
        
        return accumulators.count()
    
    @classmethod
    def first(cls, expression:Any)->str:
        """Returns the $first operator"""
        
        return accumulators.first(expression)
    
    @classmethod
    def last(cls, expression:Any)->str:
        """Returns the $last operator"""
        
        return accumulators.last(expression)
    
    @classmethod
    def max(cls, expression:Any)->str:
        """Returns the $max operator"""
        
        return accumulators.max(expression)
    
    @classmethod
    def min(cls, expression:Any)->str:
        """Returns the $min operator"""
        
        return accumulators.min(expression)
    
    @classmethod
    def push(cls, expression:Any)->str:
        """Returns the $push operator"""
        
        return accumulators.push(expression)
    
    @classmethod
    def sum(cls, expression:Any)->str:
        """Returns the $sum operator"""
        
        return accumulators.sum(expression)
    
        # Array
        # --------------------------
    @classmethod
    def array_to_object(cls, expression:Any)->str:
        """Returns the $arrayToObject operator"""

        return array.array_to_object(expression)
    
    # TODO : Workout aliases <VM, 10/08/2023>
    @classmethod
    def filter(cls, expression:Any,*, let:str, query:Any, limit:int|None=None)->str:
        """Returns the $filter operator"""

        return array.filter(expression, let, query, limit)
    
    @classmethod
    def in_(cls, left:Any, right:Any)->str:
        """Returns the $in operator"""

        return array.in_(left, right)
    
    @classmethod
    def is_array(cls, expression:Any)->str:
        """Returns the $isArray operator"""

        return array.is_array(expression)
    
    @classmethod
    def max_n(cls, expression:Any, n:int=1)->str:
        """Returns the $max operator"""

        return array.max_n(expression, n)
    
    @classmethod
    def min_n(cls, expression:Any, n:int=1)->str:
        """Returns the $min operator"""

        return array.min_n(expression, n)
    
    @classmethod
    def size(cls, expression:Any)->str:
        """Returns the $size operator"""

        return array.size(expression)
    
    # TODO : Check if the type of the sort_spec is correct <VM, 10/08/2023>
    # or can it be an expression that needs to evaluate to a dict[str, 1,-1]
    @classmethod
    def sort_array(cls, expression:Any, sort_spec:dict[str, Literal[1,-1]])->str:
        """Returns the $sort operator"""

        return array.sort_array(expression, sort_spec)

        # Comparison
        # --------------------------
    @classmethod
    def cmp(cls, left:Any, right:Any)->str:
        """Returns the $cmp operator"""

        return comparison.cmp(left, right)
    
    @classmethod
    def eq(cls, left:Any, right:Any)->str:
        """Returns the $eq operator"""

        return comparison.eq(left, right)
    
    @classmethod
    def gt(cls, left:Any, right:Any)->str:
        """Returns the $gt operator"""

        return comparison.gt(left, right)

    @classmethod
    def gte(cls, left:Any, right:Any)->str:
        """Returns the $gte operator"""

        return comparison.gte(left, right)
    
    @classmethod
    def lt(cls, left:Any, right:Any)->str:
        """Returns the $lt operator"""

        return comparison.lt(left, right)
    
    @classmethod
    def lte(cls, left:Any, right:Any)->str:
        """Returns the $lte operator"""

        return comparison.lte(left, right)
    
    @classmethod
    def ne(cls, left:Any, right:Any)->str:
        """Returns the $ne operator"""

        return comparison.ne(left, right)
    
        # Objects
        # --------------------------
    @classmethod
    def merge_objects(cls, *args:Any)->str:
        """Returns the $mergeObjects operator"""

        return objects.merge_objects(*args)
    
    @classmethod
    def object_to_array(cls, expression:Any)->str:
        """Returns the $objectToArray operator"""

        return objects.object_to_array(expression)

        # Boolean
        # --------------------------
    @classmethod
    def and_(cls, *args:Any)->str:
        """Returns the $and operator"""

        return boolean.and_(*args)
    
    @classmethod
    def or_(cls, *args:Any)->str:
        """Returns the $or operator"""

        return boolean.or_(*args)
    
    @classmethod
    def not_(cls, expression:Any)->str:
        """Returns the $not operator"""

        return boolean.not_(expression)
    
