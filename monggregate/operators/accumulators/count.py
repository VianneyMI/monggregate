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
    Creates a $count expression.
    """



    @property
    def statement(self) -> dict:

        return {
            "$count" : {}
        }

def count()->dict:
    """Creates a $count statement"""

    return Count().statement

