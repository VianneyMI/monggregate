"""Module describing the content/statement of an expression"""

from typing import Any
from monggregate.expressions.fields import FieldPath, Variable
from monggregate.operators.operator import Operator

Literal = int | float | str | bool # TODO : Change name to avoid confusion with Literal operator
Literals = list[int] | list[float] | list[str] | list[bool]
Content = Operator | dict[str, Any] | Variable | FieldPath | int | float | str | bool #| None
# dict[str, Any] above represents Operator Expressions, Expression Objects and nested expressions
