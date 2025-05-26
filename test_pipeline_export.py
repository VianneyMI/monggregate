# /!\    /!\    /!\
# Imports
# and boilerplate code
# to get the db object 
# are not included
# /!\    /!\    /!\

from monggregate import Pipeline
from pymongo import MongoClient

client = MongoClient(MONGODB_URI)
db = client["sample_mflix"]
cursor = db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
documents = list(cursor)

# The reviewer_id whose reviews we want to retrieve
reviewer_id = "2961855"

# Building the pipeline
pipeline = Pipeline()
pipeline.unwind(
    "reviews"
    ).replace_root(
        "reviews"
    ).match(
        reviewer_id=reviewer_id
    )



# Executing the pipeline
cursor = db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
documents = list(cursor)