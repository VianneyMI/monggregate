"""Expressions Module"""

# https://github.com/pydantic/pydantic/issues/2279
# https://stackoverflow.com/questions/53638973/recursive-type-annotations
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python

# TO HELP REFACTOR: https://www.practical-mongodb-aggregations.com/guides/expressions.html

# Standard Library imports
#----------------------------
from typing import Any, Literal

# 3rd Party imports
# ---------------------------
from monggregate.base import BaseModel, pyd

# Local imports
# ----------------------------
from monggregate.fields import FieldPath, Variable
from monggregate.operators.accumulators import(
    Avg,
    Count,
    First,
    Last,
    Max,
    Min,
    Push,
    Sum
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
from monggregate.operators.boolean import And, Or, Not
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
    def constant(cls, value:int | float | str | bool | None)->"Expression":
        """Creates a constant expression."""

        return cls(content=value)
    
    @classmethod
    def field(cls, name:str)->"Expression":
        """Creates a field expression."""

        if not name.startswith("$"):
            name = f"${name}"

        return cls(content=FieldPath(name=name))
    

    @classmethod
    def variable(cls, name:str)->"Expression":
        """Creates a variable expression."""

        while not variable.startswith("$$"):
            variable = "$" + variable

        return cls(content=Variable(name=name))
    

    #---------------------------------------------------
    # Logical Operators
    #---------------------------------------------------
    def __and__(self, other:"Expression")->"Expression":
        """
        Creates an And operator expression.

        Overloads python bitwise AND operator ($).
        """

       
        self.content = And(expressions=[self, other]).statement
        return self

    def __or__(self, other:"Expression")->"Expression":
        """
        Creates an Or operator expression.

        Overloads python bitwise OR operator (|).
        """

       
        self.content = Or(expressions=[self, other]).statement
        return self

    def __invert__(self)->"Expression":
        """
        Creates an Not operator expression.

        Overloads the python bitwise NOT operator (~).
        """

       
        self.content = Not(expression=self)
        return self

    #---------------------------------------------------
    # Comparison Operators
    #---------------------------------------------------
    def __eq__(self, other:"Expression")->"Expression":
        """
        Creates a $eq expression.

        Overloads python Equal to operator (==).
        """

       
        self.content = Eq(left=self, right=other)
        return self

    def __lt__(self, other:"Expression")->"Expression":
        """
        Creates a $lt expression.

        Overloads python Less than operator (<).
        """

       
        self.content = Lt(left=self, right=other)
        return self

    def __le__(self, other:"Expression")->"Expression":
        """
        Creates a $le expression.

        Overloads python Less than or equal to operator (<=).
        """

       
        self.content = Lte(left=self, right=other)
        return self

    def __gt__(self, other:"Expression")->"Expression":
        """
        Creates a $gt expression.

        Overloads python Greater than operator (>).
        """

       
        self.content = Gt(left=self, right=other)
        return self

    def __ge__(self, other:"Expression")->"Expression":
        """
        Creates a $gte expression.

        Overloads python Greather than or equal to operator (>=).
        """

       
        self.content = Gte(left=self, right=other)
        return self

    def __ne__(self, other:"Expression")->"Expression":
        """
        Creates a $lt expression.

        Overloads python Not equal to operator (!=).
        """

       
        self.content = Ne(left=self, right=other)
        return self

    def compare(self, other:"Expression")->"Expression":
        """Creates a $cmp expression."""

       
        self.content = Cmp(left=self, right=other)
        return self

    #---------------------------------------------------
    # Accumulators (Aggregation) Operators
    #---------------------------------------------------
    def average(self)->"Expression":
        """Creates an $avg expression"""

       
        self.content = Avg(expression=self)
        return self

    def count(self)->"Expression":
        """Creates a $count expression"""

       
        self.content = Count()
        return self

    def first(self)->"Expression":
        """Creates a $first expression"""

       
        self.content = First(expression=self)
        return self

    def last(self)->"Expression":
        """Creates a $last expression"""

       
        self.content = Last(expression=self)
        return self

    def max(self)->"Expression":
        """Creates a $max expression"""

       
        self.content = Max(expression=self)
        return self

    def min(self)->"Expression":
        """Creates a $min expression"""

       
        self.content = Min(expression=self)
        return self

    def push(self)->"Expression":
        """Creates a $push expression"""

       
        self.content = Push(expression=self)
        return self

    def sum(self)->"Expression":
        """Creates a $sum expression"""

        self.content = Sum(expression=self)
        return self

    #---------------------------------------------------
    # Array Operators
    #---------------------------------------------------
    def array_to_object(self)->"Expression":
        """Creates a $arrayToObject expression"""

       
        self.content = ArrayToObject(expression=self)
        return self

    def in_(self, right:"Expression")->"Expression":
        """Creates a $in operator"""

       
        self.content = In(left=self, right=right)
        return self

    def __contains__(self, right:"Expression")->"Expression":
        """Creates a $in expression"""

        return self.in_(right=right)

    def filter(self, query:"Expression", let:str|None=None, limit:int|None=None)->"Expression":
        """"Creates a $filter expression"""

       
        self.content = Filter(
            expression=self,
            query=query,
            let=let,
            limit=limit
        )
        return self

    def is_array(self)->"Expression":
        """Creates a $isArray expression"""

       
        self.content = IsArray(expression=self)
        return self

    def max_n(self, limit:int=1)->"Expression":
        """Creates a $maxN expression"""

       
        self.content = MaxN(expression=self, limit=limit)
        return self

    def min_n(self, limit:int=1)->"Expression":
        """Creates a $maxN expression"""

       
        self.content = MinN(expression=self, limit=limit)
        return self

    def sort_array(self, by:dict[str, Literal[1, -1]])->"Expression":
        """Creates a $sortArray expression"""

       
        self.content = SortArray(expression=self, by=by)
        return self

    #---------------------------------------------------
    # Objects Operators
    #---------------------------------------------------
    def merge_objects(self, )->"Expression":
        """Creates a $mergeObjects operator"""

       
        self.content = MergeObjects(expression=self)
        return self

    def object_to_array(self, )->"Expression":
        """Creates a $objectToArray operator"""

       
        self.content = ObjectToArray(expression=self)
        return self

if __name__ == "__main__":
    result = Expression(field="left") & Expression(field="right")
    print(result)

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
