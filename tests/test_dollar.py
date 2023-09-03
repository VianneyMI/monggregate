"""Module to test dollar singleton class"""

from monggregate.dollar import Dollar, DollarDollar, S, SS
from monggregate.operators import And
  
def test_dollar_getattr()->None:
    """Tests the access all class"""

    assert S.name == "$name"
    assert S.age == "$age"
    assert S.address == "$address"
  
    assert S.and_(True, True) == And(expressions=[True, True])

def test_singletons()->None:
    """Tests that Dollar and DollarDollar are singletons"""

    assert Dollar() is Dollar()
    assert DollarDollar() is DollarDollar()
    assert S is Dollar()
    assert SS is DollarDollar()

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
    test_singletons()
    test_dollar_getattr()
    test_simple_expressions()
    print("Everything passed")