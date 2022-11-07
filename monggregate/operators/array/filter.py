"""Module defining an interface to $filter operator"""

from pydantic import validator, Field
from monggregate.expressions import Expression
from monggregate.operators.array.array import ArrayOperator

class Filter(ArrayOperator):
    """
    Creates a $filter expression


    Attributes
    --------------------------------
        - array / input, Expression :  An expression that resolves to an array
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

    array : Expression =  Field(alias="input")
    query : Expression = Field(alias="cond")
    name : str | None = Field("this", alias="as")
    limit : Expression | None = Field(ge=1)

    # TODO : Add a validator in package parent class to automatically translate expressions to their statement when used as arguments <VM, 07/11/2022>
    @property
    def statement(self) -> dict:
        return {
            "$first":{
               "input" : self.array,
               "cond" : self.query,
               "as" : self.name,
               "limit" : self.limit
            }
        }

def filter(array:Expression)->dict: # pylint: disable=redefined-builtin
    """Returns a $filter statement"""

    return Filter(
        expression = array
    ).statement
