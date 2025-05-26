""""test de la fonction feature scenario"""

import os
import pytest
import pymongo
from monggregate import Pipeline
from dotenv import load_dotenv

def set_feature_scenario():

    scenario = {
        "title": "The Charge of the Light Brigade",
    }
    expected_results = [
        {
            "title": "The Charge of the Light Brigade",
            "year": 1936,
            'genres': ['Action', 'Adventure', 'Romance']
        }
    ]
    return scenario, expected_results
    
def test_for_scenario():
    # Setup
    scenario, expected_results = set_feature_scenario()
    load_dotenv(verbose=True)

    MONGODB_URI = os.environ["MONGODB_URI"]

    pipeline = Pipeline()
    pipeline.match(query=scenario).sort(by="year").limit(value=1).project(include=["title", "year", "genres"], exclude="_id")

    # Act
    client = pymongo.MongoClient(MONGODB_URI)
    db = client["sample_mflix"] 
    cursor = db["embedded_movies"].aggregate(pipeline.export())
    results = list(cursor)

    # Assert
    assert results == expected_results
    print(results)