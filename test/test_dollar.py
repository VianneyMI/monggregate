"""Module to test dollar singleton class"""

from monggregate.operators.dollar import S
from pydantic import BaseModel

class AccessAll(BaseModel):
    x:int = 1

    def merge_objects(self, *args, **kwargs):

        
        kwargs.update({"args":args})
        return kwargs

    def __getattr__(self, name):

        if name not in AccessAll.__dict__:
            output = f"${name}"
        else:
            output = AccessAll.__dict__[name]
        
        return output
    
def test_access_all()->None:
    """Tests the access all class"""

    assert AccessAll().name == "$name"
    assert AccessAll().age == "$age"
    assert AccessAll().address == "$address"
    assert AccessAll().x == 1
    assert AccessAll().merge_objects(1,2) == {"args":(1,2)}


def test_simple_expressions()->None:
    """Tests some simple expressions"""

    assert S.sum(1).statement == {"$sum": 1}

    assert S.type_("number").statement == {"$type": "number"}

    #S.avg(S.multiply(S.price, S.quantity)).statement == {"$avg": [{"$multiply": ["$price", "$quantity"]}]}

    # S.avg(S.quantity).statement == {"$avg": "$quantity"}

    # S.first(S.date).statement == {"$first": "$date"}

    # S.merge_objects([
    #     S.array_elem_at(S.from_items, 0),SS.ROOT
    # ]).statement == {"$mergeObjects": [{"$arrayElemAt": ["$fromItems", 0]}, "$$ROOT"]}

    # S.map(
    #     input=S.quizzes,
    #     as_="grade",
    #     in_=S.add(SS.grade, 2)
    # ).statement == {"$map": {"input": "$quizzes", "as": "grade", "in": {"$add": ["$$grade", 2]}}}


if __name__ == "__main__":
    test_access_all()
    test_simple_expressions()
    print("Everything passed")