"""Expressions Module"""

# https://github.com/pydantic/pydantic/issues/2279
# https://stackoverflow.com/questions/53638973/recursive-type-annotations
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python

# TO HELP REFACTOR: https://www.practical-mongodb-aggregations.com/guides/expressions.html

# Standard Library imports
#----------------------------
from typing import Any, Literal
from typing_extensions import Self

# 3rd Party imports
# ---------------------------
from monggregate.base import BaseModel, pyd

# Local imports
# ----------------------------
from monggregate.fields import FieldPath, Variable
from monggregate.operators import(
    accumulators,
    arithmetic,
    array,
    boolean,
    comparison,
    conditional,
    date,
    objects,
    strings,  
    type_,
)
#Expressions can include field paths, literals, system variables, expression objects, and expression operators. Expressions can be nested.
#ExpressionObjects {field1: Expression}
#OperatorExpression {operator:[arg, .. argN]} or {operator:arg}


class Expression(BaseModel):
    """
    MongoDB expression interface.

    Expressions can include field paths, literals, systems variables, expression objects of the form {field1: Expression}
    and expression operators of the form {operator:[arg, .. argN]} or {operator:arg}.

    Expressions can be nested.
    """

    content : Any

    @property
    def statement(self)->Any:
        return self.resolve(self.content)

    #----------------------------------------------------
    # Expression Internal Methods
    #----------------------------------------------------
    @classmethod
    def constant(cls, value:int | float | str | bool | None)->Self:
        """Creates a constant expression."""

        return cls(content=value)
    
    @classmethod
    def field(cls, name:str)->Self:
        """Creates a field expression."""

        if not name.startswith("$"):
            name = f"${name}"

        return cls(content=FieldPath(name))
    

    @classmethod
    def variable(cls, name:str)->Self:
        """Creates a variable expression."""

        while not variable.startswith("$$"):
            variable = "$" + variable

        return cls(content=Variable(name))
    

    #---------------------------------------------------
    # Logical Operators
    #---------------------------------------------------
    def __and__(self, other:Self)->Self:
        """
        Creates an And operator expression.

        Overloads python bitwise AND operator ($).
        """

       
        return self.__class__(content=boolean.And(expressions=[self, other]))
        

    def __or__(self, other:Self)->Self:
        """
        Creates an Or operator expression.

        Overloads python bitwise OR operator (|).
        """

       
        return self.__class__(content=boolean.Or(expressions=[self, other]))
       

    def __invert__(self)->Self:
        """
        Creates an Not operator expression.

        Overloads the python bitwise NOT operator (~).
        """

       
        return  self.__class__(content=boolean.Not(expression=self))


    #---------------------------------------------------
    # Comparison Operators
    #---------------------------------------------------
    def __eq__(self, other:Self)->Self:
        """
        Creates a $eq expression.

        Overloads python Equal to operator (==).
        """

       
        return self.__class__(content=comparison.Eq(left=self, right=other))
        

    def __lt__(self, other:Self)->Self:
        """
        Creates a $lt expression.

        Overloads python Less than operator (<).
        """

       
        return  self.__class__(content=comparison.Lt(left=self, right=other))
      

    def __le__(self, other:Self)->Self:
        """
        Creates a $le expression.

        Overloads python Less than or equal to operator (<=).
        """

       
        return  self.__class__(content=comparison.Lte(left=self, right=other))
        

    def __gt__(self, other:Self)->Self:
        """
        Creates a $gt expression.

        Overloads python Greater than operator (>).
        """

       
        return self.__class__(content=comparison.Gt(left=self, right=other))
        

    def __ge__(self, other:Self)->Self:
        """
        Creates a $gte expression.

        Overloads python Greather than or equal to operator (>=).
        """

       
        return self.__class__(content=comparison.Gte(left=self, right=other))
        

    def __ne__(self, other:Self)->Self:
        """
        Creates a $lt expression.

        Overloads python Not equal to operator (!=).
        """

       
        return  self.__class__(content=comparison.Ne(left=self, right=other))
        

    def compare(self, other:Self)->Self:
        """Creates a $cmp expression."""

       
        return  self.__class__(content=comparison.Cmp(left=self, right=other))
        

    #---------------------------------------------------
    # Accumulators (Aggregation) Operators
    #---------------------------------------------------
    def average(self)->Self:
        """Creates an $avg expression"""

       
        return self.__class__(content=accumulators.Avg(expression=self))
        

    def count(self)->Self:
        """Creates a $count expression"""

       
        return self.__class__(content=accumulators.Count())
        

    def first(self)->Self:
        """Creates a $first expression"""

       
        return  self.__class__(content=accumulators.First(expression=self))
        

    def last(self)->Self:
        """Creates a $last expression"""

       
        return self.__class__(content=accumulators.Last(expression=self))
        

    def max(self)->Self:
        """Creates a $max expression"""

       
        return self.__class__(content=accumulators.Max(expression=self))
        

    def min(self)->Self:
        """Creates a $min expression"""

       
        return self.__class__(content=accumulators.Min(expression=self))
        

    def push(self)->Self:
        """Creates a $push expression"""

       
        return  self.__class__(content=accumulators.Push(expression=self))
        

    def sum(self)->Self:
        """Creates a $sum expression"""

        return  self.__class__(content=accumulators.Sum(expression=self))
        

    #---------------------------------------------------
    # Array Operators
    #---------------------------------------------------
    def array_to_object(self)->Self:
        """Creates a $arrayToObject expression"""

       
        return self.__class__(content=array.ArrayToObject(expression=self))
        
    
    def in_(self, right:Self)->Self:
        """Creates a $in operator"""

       
        return  self.__class__(content=array.In(left=self, right=right))
        

    def __contains__(self, right:Self)->Self:
        """Creates a $in expression"""

        return self.__class__(content=array.In(left=self, right=right))

    def filter(self, query:Self, let:str|None=None, limit:int|None=None)->Self:
        """"Creates a $filter expression"""

       
        return  self.__class__(content=array.Filter(
            expression=self,
            query=query,
            let=let,
            limit=limit
        ))
        

    def is_array(self)->Self:
        """Creates a $isArray expression"""

       
        return self.__class__(content=array.IsArray(expression=self))
        

    def max_n(self, limit:int=1)->Self:
        """Creates a $maxN expression"""

       
        return self.__class__(content=array.MaxN(expression=self, limit=limit))
        

    def min_n(self, limit:int=1)->Self:
        """Creates a $maxN expression"""

       
        return self.__class__(content=array.MinN(expression=self, limit=limit))
        

    def sort_array(self, by:dict[str, Literal[1, -1]])->Self:
        """Creates a $sortArray expression"""

       
        return self.__class__(content=array.SortArray(expression=self, by=by))
        

    #---------------------------------------------------
    # Objects Operators
    #---------------------------------------------------
    def merge_objects(self)->Self:
        """Creates a $mergeObjects operator"""

       
        return self.__class__(content=objects.MergeObjects(expression=self))
        

    def object_to_array(self)->Self:
        """Creates a $objectToArray operator"""

       
        return self.__class__(content=objects.ObjectToArray(expression=self))
        

if __name__ == "__main__":
    result = Expression.field("left") & Expression.field("right")
    print(result())

# Examples of expression:

{"$sum":1}

{"$type" : "number"}

{ "$avg": { "$multiply": [ "$price", "$quantity" ] } } # awesome example

{ "$avg": "$quantity" }

{ "$first": "$date" }

{ "$mergeObjects": [ { "$arrayElemAt": [ "$fromItems", 0 ] }, "$$ROOT" ] }

{
    "$map":
        {
        "input": "$quizzes",
        "as": "grade",
        "in": { "$add": [ "$$grade", 2 ] }
        }
}
