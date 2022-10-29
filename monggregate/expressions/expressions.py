"""Expressions Module"""

# https://github.com/pydantic/pydantic/issues/2279
# https://stackoverflow.com/questions/53638973/recursive-type-annotations
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python

# Standard Library imports
#----------------------------
from typing import Any
#from numbers import Number
# 3rd Party imports
# ---------------------------

# Package imports
# ---------------------------
from monggregate.expressions.miscellaneous import FieldPath, AggregationVariables,  Literal_
from monggregate.operators.operator import OperatorEnum

# Typing
# ----------------------------
    # Operator expressions
    # ------------------------
    # Operator expressions are similar to functions that take arguments.
    # In general, these expressions take an array of arguments and have the following form:
        # { <operator>: [ <argument1>, <argument2> ... ] }
    # If operator accepts a single argument, you can omit the outer array designating the argument list:
        # { <operator>: <argument> }

OperatorArgumentTypes = int | float | str | bool # Possible types for operator epressions # TODO : Replace int and float by number <VM, 28/10/2022>
                                            # each OperatorArgument can be a FieldPath or an expression
                                            # that must resolve (i.e evaluates) to the below types
                                            # or be a variable of this type directly
                                            # for example {"$abs":-1} is a valid operator expression

OperatorArgumentsTypes =  list[int] | list[float] | list[str] | list[bool]
OperatorArguments = OperatorArgumentTypes | OperatorArgumentsTypes | FieldPath | list[FieldPath] | dict[FieldPath, Any]

OperatorExpression = dict[OperatorEnum, OperatorArguments]

    # Expression Object
    # -------------------------
    #Expression objects have the following form:
        # { <field1>: <expression1>, ... }
    # If the expressions are numeric or boolean literals, MongoDB treats the literals as projection flags (e.g. 1 or true to include the field), valid only in the
    # $project stage. To avoid treating numeric or boolean literals as projection flags, use the
    # $literal expression to wrap the numeric or boolean literals.
ExpressionObject = dict[FieldPath, Any]

    # Expressions
    # ------------------------
    # Expressions can include field paths, literals, system variables, expression objects, and expression operators.
    # Expressions can be nested.
    # (You can have expressions in OperatorExpression and ExpressionObject)

Expression = FieldPath | list[FieldPath] | AggregationVariables | OperatorExpression | ExpressionObject | Literal_

# TODO : Define more precise types for OperatorArguments, ExpressionObject and Expression when pydantic allows recursive types <VM, 05/10/2022>
