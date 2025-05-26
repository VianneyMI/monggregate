""""test de la fonction feature scenario"""

import os
import pytest
import pymongo
from monggregate import Pipeline
from dotenv import load_dotenv

def set_feature_scenario():

    scenario = {
        "title": "A Star Is Born",
        "year": 2018
    }
    expected_results = [
        {
            "_id": 1,
            "title": "A Star Is Born",
            "year": 2018
        }
    ]
    return scenario, expected_results
    
def test_for_scenario():
    # Setup
    scenario, expected_results = set_feature_scenario()
    load_dotenv(verbose=True)

    MONGODB_URI = os.environ["MONGODBPASSWORD"]

    pipeline = Pipeline()
    pipeline.match(title=scenario["title"]).sort(by="year").limit(value=1)

    # Act
    client = pymongo.MongoClient(MONGODB_URI)
    db = client["mydatabase"] 
    cursor = db["movies"].aggregate(pipeline.export())
    results = list(cursor)

    # Assert
    assert results == expected_results
    print(results)