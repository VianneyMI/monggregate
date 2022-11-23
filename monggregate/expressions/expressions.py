"""Expressions Module"""

# https://github.com/pydantic/pydantic/issues/2279
# https://stackoverflow.com/questions/53638973/recursive-type-annotations
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python

# Standard Library imports
#----------------------------
from typing import Any
from monggregate.base import BaseModel
from monggregate.expressions.field_paths import FieldPath, Variable
from monggregate.operators.boolean import And, Or, Not
#from numbers import Number
# 3rd Party imports
# ---------------------------

#Expressions can include field paths, literals, system variables, expression objects, and expression operators. Expressions can be nested.
#ExpressionObjects {field1: Expression}
#OperatorExpression {operator:[arg, .. argN]} or {operator:arg}


class Expression(BaseModel):
    """Expression Generator"""

    field : FieldPath | None
    variable : Variable | None
    constant : int | float | str | None
    key : str | None
    value : "Expression" | None
    document : dict[str, "Expression"] | None


    @property
    def statement(self)->Any:
        return self.field


    def __and__(self, other:"Expression")->dict:
        """Python $ (and) operator overload"""

        return And(expressions=[self, other]).statement

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