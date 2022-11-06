"""
Module defining an interface to MongoDB $avg accumulator operator

Online MongoDB documentation:
--------------------------------------------------------------------------------------------------------------------
Last Updated (in this package) : 06/11/2022
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/count-accumulator/#mongodb-group-grp.-count

"""


from monggregate.operators.accumulators.accumulator import Accumulator

class Count(Accumulator):
    """
    Creates a sum expression.
    """



    @property
    def statement(self) -> dict:

        return {
            "$push" : self.expression
        }

def count()->dict:
    """Creates a push statement"""

    return Count().statement

