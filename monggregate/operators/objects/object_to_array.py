"""Module defining an interface to $mergeObjects operator"""

from monggregate.operators.array.array import ArrayOperator

class ObjectToArray(ArrayOperator):
    """Creates an $arrayToObject expression"""

    document : dict

    @property
    def statement(self) -> dict:
        return {
            "$objectToArray" : self.document
        }

def object_to_array(document:dict)->dict:
    """Returns a *objectToArray statement"""

    return ObjectToArray(document=document).statement
