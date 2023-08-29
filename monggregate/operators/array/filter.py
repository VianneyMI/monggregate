"""
Module defining an interface to $filter operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------

Last Updated (in this package) : 12/11/2022
Source :  https://www.mongodb.com/docs/manual/reference/operator/aggregation/filter/#mongodb-expression-exp.-filter

Definition
----------------------------------------
$filter
Selects a subset of an array to return based on the specified condition.
Returns an array with only those elements that match the condition.
The returned elements are in the original order.

$filter has the following syntax:

>>> {
   $filter:
      {
         input: <array>,
         cond: <expression>,
         as: <string>,
         limit: <number expression>
      }
}

* input : An expression that resolves to an array.
* cond : An expression that resolves to a boolean value used to determine if an element should be included in the
         output array. The expression references each element of the input array individually with the variable name
         specified in as.
* as : Optional. A name for the variable that represents each individual element of the input array.
       If no name is specified, the variable name defaults to this.
* limit : Optional. A number expression that restricts the number of matching array elements that
          $filter returns.
          You cannot specify a limit less than 1.
          The matching array elements are returned in the order they appear in the input array.

          If the specified limit is greater than the number of matching array elements,
          $filter returns all matching array elements. If the limit is null,
          $filter returns all matching array elements.
"""

from typing import Any
from monggregate.base import pyd
from monggregate.operators.array.array import ArrayOperator

class Filter(ArrayOperator):
    """
    Creates a $filter expression


    Attributes
    --------------------------------
        - expression / input, Expression :  An expression that resolves to an array
        - query / cond, Expression : An expressions that resolves to a boolean value used to determine
                                     if an element should be included in the output array. The expression
                                     references each element of the input array individually with the variable
                                     name specified in as.
        - name / as, str : A name for the variable that represents each individual element of the input array.
                                  If no name is specified, the variable name defaults to this.
        - limit , int | None : An optional number expression that restricts the number of matching array elements that $filter return.
                               You cannot specify a limit less than 1.
                               The matching array elements are returned in the order they appear in the input array.
                               If the specified limit is greather than the number of matching array elements, $filter returns all matching
                               array elements. If the limit is null,$filters returns all matching array elements.

    """

    expression : Any =  pyd.Field(alias="input")
    query : Any = pyd.Field(alias="cond")
    let : str | None = pyd.Field("this", alias="as")
    limit : int | None = pyd.Field(None, ge=1) # NOTE : limit can actually be an expression but constraints are  invalid with any type

    @property
    def statement(self) -> dict:
        return self.resolve({
            "$filter":{
               "input" : self.expression,
               "cond" : self.query,
               "as" : self.let,
               "limit" : self.limit
            }
        })

def filter(expression:Any, let:str, query:Any, limit:int|None=None)->Filter: 
    """Returns a $filter operator"""

    return Filter(
        expression = expression,
        query = query,
        let = let,
        limit = limit
    )
