import os
import json
from monggregate import Pipeline
from pymongo import MongoClient
from bson import json_util
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def test_pipeline_dblistingsAndReviews():
    # Setup
    MONGODB_URI = os.environ["MONGODB_URI"]
    client = MongoClient(MONGODB_URI)
    db = client["sample_airbnb"]

    reviewer_id = "2961855"

    path_to_expected_documents = Path(__file__).parent / "data" / "test_pipeline_reviews_results.json"
    with open(path_to_expected_documents, "r") as file:
        expected_documents = json.load(file)


    # Pipeline création du reviewer
    pipeline = Pipeline()
    pipeline.unwind(
        "reviews"
    ).replace_root(
        "reviews"
    ).match(
        reviewer_id=reviewer_id
    )

    # Act
    cursor = db[reviewer_id].aggregate(pipeline=pipeline.export())
    documents = list(cursor)
    expected_documents = json.loads(json_util.dumps(documents))

    # Assert
    assert documents == expected_documents


if __name__ == "__main__":
    test_pipeline_dblistingsAndReviews()