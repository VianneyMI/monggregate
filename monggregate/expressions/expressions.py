"""Expressions Module"""

from numbers import Number

from monggregate.expressions.miscellaneous import FieldPath, Literal_
from monggregate.operators.operator import OperatorEnum

OperatorArguments = FieldPath | list[FieldPath] #| Number # TODO : Complete Union here <VM, 30/09/2022>
OperatorExpression = dict[OperatorEnum, OperatorArguments]

ExpressionObject = dict[FieldPath, "Expression"]
Expression = FieldPath | OperatorExpression | ExpressionObject

# Expressions
# ----------------------------------
# Expressions can include field paths, literals, system variables,
# expression objects, and expression operators.

# Expressions can be nested.
