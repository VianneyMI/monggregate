"""Module describing the content/statement of an expression"""

from typing import Any
from monggregate.expressions.fields import FieldPath, Variable
#from monggregate.operators.operator import Operator

# TODO  : Distinguish between expressions evaluations (evaluated expressions) and lazy expressions (expressions that are not evaluated)
Const = int | float | str | bool
Consts = list[int] | list[float] | list[str] | list[bool]
Content = dict[str, Any] | Variable | FieldPath | int | float | str | bool | list[int] | list[float] | list[str] | list[bool]
# dict[str, Any] above represents Operator Expressions, Expression Objects and nested expressions

# In all these cases, an expression is just something that dynamically populates and returns a new JSON/BSON data type element, which can be one of:

    # * a Number  (including integer, long, float, double, decimal128)
    # * a String  (UTF-8)
    # * a Boolean
    # * a DateTime  (UTC)
    # * an Array
    # * an Object

# In a nutshell (Vianney's words): Expressions are lazily evaluated objects


# The previously stated generalisation about $match not supporting expressions is actually inaccurate. 
# Version 3.6 of MongoDB introduced the $expr operator, which you can embed within a $match stage (or in MQL) to leverage aggregation expressions when filtering records. 
# Essentially, this enables MongoDB's query runtime (which executes an aggregation's $match) to reuse expressions provided by MongoDB's aggregation runtime.

# Inside a $expr operator, you can include any composite expression fashioned from $ operator functions, 
# $ field paths and $$ variables. A few situations demand having to use $expr from inside a $match stage. Examples include: