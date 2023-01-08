"""Expressions Module"""

# https://github.com/pydantic/pydantic/issues/2279
# https://stackoverflow.com/questions/53638973/recursive-type-annotations
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python

# Standard Library imports
#----------------------------
from typing import Any, Literal

# 3rd Party imports
# ---------------------------
from pydantic import validator

# Local imports
# ----------------------------
from monggregate.base import BaseModel
from monggregate.expressions.fields import FieldPath, Variable
from monggregate.expressions.content import Content
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

    constant : int | float | str | bool | None
    field : FieldPath | None
    variable : Variable | None

    content : Content | None

    @validator("variable", pre=True, always=True)
    @classmethod
    def validate_variable(cls, variable:str|None) -> Variable | None:
        """Validates variable"""

        if variable:
            while not variable.startswith("$$"):
                variable = "$" + variable

        return variable

    @validator("field", pre=True, always=True)
    @classmethod
    def validate_field(cls, path:str|None)-> FieldPath | None:
        """Validates field"""

        if path and not path.startswith("$"):
            path =  "$" + path

        return path

    @validator("content", pre=True, always=True)
    @classmethod
    def set_content(cls, content:Any, values:dict)->Content:
        """Sets content by parsing values and validates it"""


        if content:
            raise ValueError("Content should no be provided")

        constant = values.get("constant")
        field = values.get("field")
        variable = values.get("variable")

        if isinstance(constant, str):
            if field:
                content = {field:constant}
            # elif variable:
            #     content = {field:variable}
            else:
                content = constant
        elif field:
            content = field
        elif variable:
            content = variable
        else:
            content = None

        return content


    @property
    def statement(self)->Any:
        return self.content

    #----------------------------------------------------
    # Expression Internal Methods
    #----------------------------------------------------
    def _clear(self)->None:
        """Empties expression"""

        self.constant = None
        self.field = None
        self.variable = None
        #self.content = None # This would break most of the
                             # functions below

    #---------------------------------------------------
    # Logical Operators
    #---------------------------------------------------
    def __and__(self, other:"Expression")->"Expression":
        """
        Creates an And operator expression.

        Overloads python bitwise AND operator ($).
        """

        #self._clear()
        self.content = And(expressions=[self, other]).statement
        return self

    def __or__(self, other:"Expression")->"Expression":
        """
        Creates an Or operator expression.

        Overloads python bitwise OR operator (|).
        """

        #self._clear()
        self.content = Or(expressions=[self, other]).statement
        return self

    def __invert__(self)->"Expression":
        """
        Creates an Not operator expression.

        Overloads the python bitwise NOT operator (~).
        """

        #self._clear()
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

        #self._clear()
        self.content = Eq(left=self, right=other)
        return self

    def __lt__(self, other:"Expression")->"Expression":
        """
        Creates a $lt expression.

        Overloads python Less than operator (<).
        """

        #self._clear()
        self.content = Lt(left=self, right=other)
        return self

    def __le__(self, other:"Expression")->"Expression":
        """
        Creates a $le expression.

        Overloads python Less than or equal to operator (<=).
        """

        #self._clear()
        self.content = Lte(left=self, right=other)
        return self

    def __gt__(self, other:"Expression")->"Expression":
        """
        Creates a $gt expression.

        Overloads python Greater than operator (>).
        """

        #self._clear()
        self.content = Gt(left=self, right=other)
        return self

    def __ge__(self, other:"Expression")->"Expression":
        """
        Creates a $gte expression.

        Overloads python Greather than or equal to operator (>=).
        """

        #self._clear()
        self.content = Gte(left=self, right=other)
        return self

    def __ne__(self, other:"Expression")->"Expression":
        """
        Creates a $lt expression.

        Overloads python Not equal to operator (!=).
        """

        #self._clear()
        self.content = Ne(left=self, right=other)
        return self

    def compare(self, other:"Expression")->"Expression":
        """Creates a $cmp expression."""

        #self._clear()
        self.content = Cmp(left=self, right=other)
        return self

    #---------------------------------------------------
    # Accumulators (Aggregation) Operators
    #---------------------------------------------------
    def average(self)->"Expression":
        """Creates an $avg expression"""

        #self._clear()
        self.content = Avg(expression=self)
        return self

    def count(self)->"Expression":
        """Creates a $count expression"""

        #self._clear()
        self.content = Count()
        return self

    def first(self)->"Expression":
        """Creates a $first expression"""

        #self._clear()
        self.content = First(expression=self)
        return self

    def last(self)->"Expression":
        """Creates a $last expression"""

        #self._clear()
        self.content = Last(expression=self)
        return self

    def max(self)->"Expression":
        """Creates a $max expression"""

        #self._clear()
        self.content = Max(expression=self)
        return self

    def min(self)->"Expression":
        """Creates a $min expression"""

        #self._clear()
        self.content = Min(expression=self)
        return self

    def push(self)->"Expression":
        """Creates a $push expression"""

        #self._clear()
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

        #self._clear()
        self.content = ArrayToObject(expression=self)
        return self

    def in_(self, right:"Expression")->"Expression":
        """Creates a $in operator"""

        #self._clear()
        self.content = In(left=self, right=right)
        return self

    def __contains__(self, right:"Expression")->"Expression":
        """Creates a $in expression"""

        return self.in_(right=right)

    def filter(self, query:"Expression", let:str|None=None, limit:int|None=None)->"Expression":
        """"Creates a $filter expression"""

        #self._clear()
        self.content = Filter(
            expression=self,
            query=query,
            let=let,
            limit=limit
        )
        return self

    def is_array(self)->"Expression":
        """Creates a $isArray expression"""

        #self._clear()
        self.content = IsArray(expression=self)
        return self

    def max_n(self, limit:int=1)->"Expression":
        """Creates a $maxN expression"""

        #self._clear()
        self.content = MaxN(expression=self, limit=limit)
        return self

    def min_n(self, limit:int=1)->"Expression":
        """Creates a $maxN expression"""

        #self._clear()
        self.content = MinN(expression=self, limit=limit)
        return self

    def sort_array(self, by:dict[str, Literal[1, -1]])->"Expression":
        """Creates a $sortArray expression"""

        #self._clear()
        self.content = SortArray(expression=self, by=by)
        return self

    #---------------------------------------------------
    # Objects Operators
    #---------------------------------------------------
    def merge_objects(self, )->"Expression":
        """Creates a $mergeObjects operator"""

        #self._clear()
        self.content = MergeObjects(expression=self)
        return self

    def object_to_array(self, )->"Expression":
        """Creates a $objectToArray operator"""

        #self._clear()
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
