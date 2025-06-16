import os
import json
from monggregate import Pipeline
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util

load_dotenv()

def test_pipeline_dbmovies():


    # Setup
    MONGODB_URI = os.environ["MONGODB_URI"]
    client = MongoClient(MONGODB_URI)
    db = client["sample_mflix"]

    MONGODB_URI = os.environ["MONGODB_URI"]
    
   

    with open("test_pipeline_stages_results.json", "r") as file:
        expected_results = json.load(file)

    # Pipeline

    pipeline = Pipeline()
    pipeline.lookup(
        right="comments", 
        left_on="_id",     
        right_on="movie_id", 
        name="related_comments"
    ).limit(10)
    # Excluding _id and limit to 10 elements for testability purposes
   
    #Act
    cursor = db["movies"].aggregate(pipeline=pipeline.export())
    results = list(cursor)
    results = json.loads(json_util.dumps(results))

    # Assert

    assert results == expected_results, results



if __name__ == "__main__":
    test_pipeline_dbmovies()