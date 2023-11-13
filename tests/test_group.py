"""Module to test group (temp)"""

#from dictdiffer import diff
from monggregate import Pipeline
from monggregate.stages.group import Group


def test_group_stage():
    """Test group stage"""

    # Test by as list
    # ------------------------------
    assert Group(
            by=["name", "age"],
            query = {
                "output":{"$sum":"income"}
            }
        ).statement == {
            "$group":{
                "_id":["$name", "$age"],
                "output":{"$sum":"income"}
            }
        }

    # Test by as set
    # ------------------------------
    group = Group(
            by={"name", "age"},
            query = {
                "output":{"$sum":"income"}
            }
        )
    
    expected_statement = {
            "$group":{
                "_id":["$age", "$name"],
                "output":{"$sum":"income"}
            }
        }
    assert  group.statement == expected_statement
    #, list(diff(expected_statement, group.statement)) 
    

    # Test by as dict
    # ------------------------------
    assert Group(
            by={"name":"$name", "age":"$age"},
            query = {
                "output":{"$sum":"income"}
            }
        ).statement == {
            "$group":{
                "_id":{"name":"$name", "age":"$age"},
                "output":{"$sum":"income"}
            }
        }

def test_group_in_pipeline():

    # Reproduce tests above with pipeline
    # -----------------------------------
    # 
    # Test by as list
    # ------------------------------

    assert Pipeline().group(
            by=["name", "age"],
            query = {
                "output":{"$sum":"income"}
            }
        ).statement == [
            {
                "$group":{
                    "_id":["$name", "$age"],
                    "output":{"$sum":"income"}
                }
            }
        ]
    
    # Test by as set
    # ------------------------------
    assert Pipeline().group(
            by={"name", "age"},
            query = {
                "output":{"$sum":"income"}
            }
        ).statement == [
            {
                "$group":{
                    "_id":["$age", "$name"],
                    "output":{"$sum":"income"}
                }
            }
        ]
    
    # Test by as dict
    # ------------------------------
    assert Pipeline().group(
            by={"name":"$name", "age":"$age"},
            query = {
                "output":{"$sum":"income"}
            }
        ).statement == [
            {
                "$group":{
                    "_id":{"name":"$name", "age":"$age"},
                    "output":{"$sum":"income"}
                }
            }
        ]

if __name__ == "__main__":
    test_group_stage()
    test_group_in_pipeline()
    print("All tests passed")
