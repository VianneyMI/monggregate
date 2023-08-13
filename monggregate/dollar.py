"""WIP"""

from typing import Any, Literal

from monggregate.base import BaseModel

from monggregate.operators import(
    accumulators,
    array,
    comparison,
    objects,
    boolean,
    type_  
)

from monggregate.utils import StrEnum

class AggregationVariableEnum(StrEnum):
    """Enumeration of available aggregation variables"""

    NOW = "$$NOW" # Returns the current datetime value,
                # which is same across all members of the deployment and remains constant throughout the aggregation pipeline.
                # (Available in 4.2+)
    CLUSTER_TIME = "$$CLUSTER_TIME" # Returns the current timestamp value, which is same across all members of the deployment and remains constant throughout the aggregation pipeline.
                                    # For replica sets and sharded clusters only. (Available in 4.2+)
    ROOT = "$$ROOT" # References the root document, i.e. the top-level document.
    CURRENT = "$$CURRENT" # References the start of the field path, which by default is ROOT but can be changed.
    REMOVE = "$$REMOVE" # Allows for the conditional exclusion of fields. (Available in 3.6+)
    DESCEND = "$$DESCEND" # One of the allowed results of a $redact expression.
    PRUNE = "$$PRUNE" # One of the allowed results of a $redact expression.
    KEEP = "$$KEEP" # One of the allowed results of a $redact expression.NOW = "$$NOW" # Returns the current datetime value,
                # which is same across all members of the deployment and remains constant throughout the aggregation pipeline.
                # (Available in 4.2+)

CLUSTER_TIME = AggregationVariableEnum.CLUSTER_TIME.value
NOW = AggregationVariableEnum.NOW.value
ROOT = AggregationVariableEnum.ROOT.value
CURRENT = AggregationVariableEnum.CURRENT.value
REMOVE = AggregationVariableEnum.REMOVE.value
DESCEND = AggregationVariableEnum.DESCEND.value
PRUNE = AggregationVariableEnum.PRUNE.value
KEEP = AggregationVariableEnum.KEEP.value

# NOTE : If dollar is to be made to really store all of MongoDB functions i.e stages, operators and whathever they come up with
# it might de interesting to create a DollarBase class, a DollarStage class and a DollarOperator class and to use inheritance <VM, 10/08/2023>
class Dollar:
    """Base class for all $ functions"""

    # Any below should be replaced by a Union of
    # all operators or by Typevar bounded by Operator
    def __getattr__(self, name)->str|Any:
        """Overloads the __getattr__ method. 
        Return the name of the attribute with a $ prepended to it
        (when it's not a method or an attribute of the classe)
        
        """

        if name not in self.__class__.__dict__:
            output = f"${name}"
        else:
            output = self.__class__.__dict__[name]

        return output

    # Operators
    # ------------------------------

        # Accumulators
        # --------------------------
    @classmethod
    def avg(cls, expression:Any)->accumulators.Avg:
        """Returns the $avg operator"""
        
        return accumulators.avg(expression)
    
    @classmethod
    def count(cls)->accumulators.Count:
        """Returns the $count operator"""
        
        return accumulators.count()
    
    @classmethod
    def first(cls, expression:Any)->accumulators.First:
        """Returns the $first operator"""
        
        return accumulators.first(expression)
    
    @classmethod
    def last(cls, expression:Any)->accumulators.Last:
        """Returns the $last operator"""
        
        return accumulators.last(expression)
    
    @classmethod
    def max(cls, expression:Any)->accumulators.Max:
        """Returns the $max operator"""
        
        return accumulators.max(expression)
    
    @classmethod
    def min(cls, expression:Any)->accumulators.Min:
        """Returns the $min operator"""
        
        return accumulators.min(expression)
    
    @classmethod
    def push(cls, expression:Any)->accumulators.Push:
        """Returns the $push operator"""
        
        return accumulators.push(expression)
    
    @classmethod
    def sum(cls, expression:Any)->accumulators.Sum:
        """Returns the $sum operator"""
        
        return accumulators.sum(expression)
    
        # Array
        # --------------------------
    @classmethod
    def array_to_object(cls, expression:Any)->array.ArrayToObject:
        """Returns the $arrayToObject operator"""

        return array.array_to_object(expression)
    
    # TODO : Workout aliases <VM, 10/08/2023>
    @classmethod
    def filter(cls, expression:Any,*, let:str, query:Any, limit:int|None=None)->array.Filter:
        """Returns the $filter operator"""

        return array.filter(expression, let, query, limit)
    
    @classmethod
    def in_(cls, left:Any, right:Any)->array.In:
        """Returns the $in operator"""

        return array.in_(left, right)
    
    @classmethod
    def is_array(cls, expression:Any)->array.IsArray:
        """Returns the $isArray operator"""

        return array.is_array(expression)
    
    @classmethod
    def max_n(cls, expression:Any, n:int=1)->array.MaxN:
        """Returns the $max operator"""

        return array.max_n(expression, n)
    
    @classmethod
    def min_n(cls, expression:Any, n:int=1)->array.MinN:
        """Returns the $min operator"""

        return array.min_n(expression, n)
    
    @classmethod
    def size(cls, expression:Any)->array.Size:
        """Returns the $size operator"""

        return array.size(expression)
    
    # TODO : Check if the type of the sort_spec is correct <VM, 10/08/2023>
    # or can it be an expression that needs to evaluate to a dict[str, 1,-1]
    @classmethod
    def sort_array(cls, expression:Any, sort_spec:dict[str, Literal[1,-1]])->array.SortArray:
        """Returns the $sort operator"""

        return array.sort_array(expression, sort_spec)

        # Comparison
        # --------------------------
    @classmethod
    def cmp(cls, left:Any, right:Any)->comparison.Cmp:
        """Returns the $cmp operator"""

        return comparison.cmp(left, right)
    
    @classmethod
    def eq(cls, left:Any, right:Any)->comparison.Eq:
        """Returns the $eq operator"""

        return comparison.eq(left, right)
    
    @classmethod
    def gt(cls, left:Any, right:Any)->comparison.Gt:
        """Returns the $gt operator"""

        return comparison.gt(left, right)

    @classmethod
    def gte(cls, left:Any, right:Any)->comparison.Gte:
        """Returns the $gte operator"""

        return comparison.gte(left, right)
    
    @classmethod
    def lt(cls, left:Any, right:Any)->comparison.Lt:
        """Returns the $lt operator"""

        return comparison.lt(left, right)
    
    @classmethod
    def lte(cls, left:Any, right:Any)->comparison.Lte:
        """Returns the $lte operator"""

        return comparison.lte(left, right)
    
    @classmethod
    def ne(cls, left:Any, right:Any)->comparison.Ne:
        """Returns the $ne operator"""

        return comparison.ne(left, right)
    
        # Objects
        # --------------------------
    @classmethod
    def merge_objects(cls, *args:Any)->objects.MergeObjects:
        """Returns the $mergeObjects operator"""

        return objects.merge_objects(*args)
    
    @classmethod
    def object_to_array(cls, expression:Any)->objects.ObjectToArray:
        """Returns the $objectToArray operator"""

        return objects.object_to_array(expression)

        # Boolean
        # --------------------------
    @classmethod
    def and_(cls, *args:Any)->boolean.And:
        """Returns the $and operator"""

        return boolean.and_(*args)
    
    @classmethod
    def or_(cls, *args:Any)->boolean.Or:
        """Returns the $or operator"""

        return boolean.or_(*args)
    
    @classmethod
    def not_(cls, expression:Any)->boolean.Not:
        """Returns the $not operator"""

        return boolean.not_(expression)
    
        # Type
        # --------------------------
    @classmethod
    def type_(cls, expression:Any)->type_.Type_:
        """Returns the $type operator"""

        return type_.type_(expression)
    
class DollarDollar:
    """xxx"""

    CLUSTER_TIME = AggregationVariableEnum.CLUSTER_TIME.value
    NOW = AggregationVariableEnum.NOW.value
    ROOT = AggregationVariableEnum.ROOT.value
    CURRENT = AggregationVariableEnum.CURRENT.value
    REMOVE = AggregationVariableEnum.REMOVE.value
    DESCEND = AggregationVariableEnum.DESCEND.value
    PRUNE = AggregationVariableEnum.PRUNE.value
    KEEP = AggregationVariableEnum.KEEP.value

    def __getattr__(self, name)->str|Any:
        """Overloads the __getattr__ method. 
        Return the name of the attribute with a $ prepended to it
        (when it's not a method or an attribute of the classe)
        
        """

        if name not in self.__class__.__dict__:
            output = f"$${name}"
        else:
            output = self.__class__.__dict__[name]

        return output


# TODO : Make below instances singletons <VM, 13/08/2023>
S = Dollar()
SS = DollarDollar()
