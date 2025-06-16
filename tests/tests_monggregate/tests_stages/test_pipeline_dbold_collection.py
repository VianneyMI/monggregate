import os
import json
from monggregate import Pipeline
from pymongo import MongoClient
from bson import json_util
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def test_pipeline_dbold_collection():
    #Setup
    load_dotenv(verbose=True)
    MONGODB_URI = os.environ["MONGODB_URI"]
    client = MongoClient(MONGODB_URI)
    db = client["sample_airbnb"]

    new_field = "review_ids"
    new_collection = "listings"
    old_collection = "listingsAndReviews"

    path_to_expected_documents = Path(__file__).parent / "data" / "test_pipeline_reviews_results.json"
    with open(path_to_expected_documents, "r") as file:
        expected_documents = json.load(file)

    # Pipeline de création de la nouvelle collection
    pipeline = Pipeline()
    pipeline.add_fields(
        {new_field: "$reviews._id"}
    ).add_fields(
        {"reviews": f"${new_field}"}
    ).unset(
        new_field
    ).out(new_collection)

    #Act
    cursor = list(db[new_field].aggregate(pipeline=pipeline.export()))
    cursor = list(db[new_collection].aggregate(pipeline=pipeline.export()))
    cursor = list(db[old_collection].aggregate(pipeline=pipeline.export()))
    documents = list(cursor)
    expected_documents = json.loads(json_util.dumps(documents))

    # Assert
    assert documents == expected_documents


if __name__ == "__main__":
    test_pipeline_dbold_collection()