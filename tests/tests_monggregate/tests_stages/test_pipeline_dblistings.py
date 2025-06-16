import os
import json
from monggregate import Pipeline
from pymongo import MongoClient
from bson import json_util
from dotenv import load_dotenv
from pathlib import Path

def test_pipeline_dblistings():
    #Setup
    load_dotenv(verbose=True)
    MONGODB_URI = os.environ["MONGODB_URI"]
    client = MongoClient(MONGODB_URI)
    db = client["sample_airbnb"]

    reviews = "reviews"

    path_to_expected_documents = Path(__file__).parent / "data" / "test_pipeline_reviews_results.json"
    with open(path_to_expected_documents, "r") as file:
        expected_documents = json.load(file)

    #Pipeline création des reviews

    pipeline = Pipeline()
    pipeline.lookup(
        right=reviews,
        left_on="reviews_id",
        right_on="_id",
        name="reviews"
    )

    # Act
    cursor = list(db[reviews].aggregate(pipeline=pipeline.export()))
    documents = list(cursor)
    expected_documents = json.loads(json_util.dumps(documents))
    
    # Assert
    assert documents == expected_documents

if __name__ == "__main__":
    test_pipeline_dblistings()